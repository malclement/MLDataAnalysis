provider "aws" {
  region = "eu-west-3"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet" "selected_subnet" {
  id = "subnet-091a8c6908070c000"
}

data "aws_subnet" "additional_subnet" {
  id = "subnet-0a293bb3a88169424"
}

# Security Group for Load Balancer
resource "aws_security_group" "alb_sg" {
  name        = "fastapi-alb-sg"
  description = "Allow HTTP inbound traffic to ALB"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "FastAPI ALB Security Group"
  }
}

# Security Group for ECS Tasks
resource "aws_security_group" "ecs_web_access_sg" {
  name        = "ecs_web_access_sg"
  description = "Allow inbound traffic from ALB and outbound traffic"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "ECS_Cluster" {
  name = "fastapi-ecs-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Environment = "dev"
    Application = "fastapi_service"
    Name        = "FASTAPI-ECS-CLUSTER"
  }
}

# IAM Role for ECS Task Execution
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecsTaskExecutionRole-customer-managed"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# IAM Policy for ECS Task Execution
resource "aws_iam_policy" "ecs_task_execution_policy" {
  name = "ecsTaskExecutionPolicy-customer-managed"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ecr:GetAuthorizationToken", "ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:ListBucket", "s3:GetObject", "s3:PutObject", "s3:DeleteObject"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret", "secretsmanager:ListSecrets", "secretsmanager:ReadSecret"]
        Resource = "*"
      }
    ]
  })
}

# Attach IAM Policy to Role
resource "aws_iam_role_policy_attachment" "ecs_task_execution_policy_attachment" {
  policy_arn = aws_iam_policy.ecs_task_execution_policy.arn
  role       = aws_iam_role.ecs_task_execution_role.name
}

# ECS Task Definition
resource "aws_ecs_task_definition" "fargate_task" {
  family                   = "fastapi-service"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_execution_role.arn
  cpu                      = "512"
  memory                   = "1024"

  runtime_platform {
    cpu_architecture        = "ARM64"
    operating_system_family = "LINUX"
  }

  container_definitions = jsonencode([
    {
      name  = "fastapi-service"
      image = "034362044212.dkr.ecr.eu-west-3.amazonaws.com/mldataanalysis:latest"
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_log_group.name
          awslogs-region        = "eu-west-3"
          awslogs-stream-prefix = "ecs"
        }
      }
      essential = true
    }
  ])
}

# Application Load Balancer
resource "aws_lb" "fastapi_alb" {
  name               = "fastapi-application-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets = [
    data.aws_subnet.selected_subnet.id,
    data.aws_subnet.additional_subnet.id
  ]

  tags = {
    Environment = "dev"
    Application = "fastapi_service"
  }
}

# Target Group for ECS Tasks
resource "aws_lb_target_group" "fastapi_tg" {
  name        = "fastapi-target-group"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.default.id
  target_type = "ip"

  health_check {
    path                = "/" # Adjust to your health check endpoint
    healthy_threshold   = 2
    unhealthy_threshold = 10
    timeout             = 60
    interval            = 300
    matcher             = "200-399"
  }
}

# ALB Listener
resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.fastapi_alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.fastapi_tg.arn
  }
}

# ECS Service
resource "aws_ecs_service" "fastapi_ecs_service" {
  name            = "fastapi-service"
  cluster         = aws_ecs_cluster.ECS_Cluster.id
  task_definition = aws_ecs_task_definition.fargate_task.arn
  desired_count   = 1

  # Removed launch_type and adjusted capacity provider strategy
  capacity_provider_strategy {
    capacity_provider = "FARGATE_SPOT"
    weight            = 100
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.fastapi_tg.arn
    container_name   = "fastapi-service"
    container_port   = 8000
  }

  network_configuration {
    subnets          = [data.aws_subnet.selected_subnet.id, data.aws_subnet.additional_subnet.id]
    security_groups  = [aws_security_group.ecs_web_access_sg.id]
    assign_public_ip = true
  }

  tags = {
    Environment = "dev"
    Application = "fastapi_service"
    Name        = "FASTAPI-ECS-SERVICE"
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "ecs_log_group" {
  name              = "/ecs/fastapi-service"
  retention_in_days = 7 # Retain logs for 7 days; adjust as needed
}

# Outputs
output "ecs_cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.ECS_Cluster.name
}

output "ecs_service_name" {
  description = "The name of the ECS service"
  value       = aws_ecs_service.fastapi_ecs_service.name
}

output "ecs_task_definition_arn" {
  description = "The ARN of the ECS task definition"
  value       = aws_ecs_task_definition.fargate_task.arn
}

output "security_group_id" {
  description = "The security group ID for ECS tasks"
  value       = aws_security_group.ecs_web_access_sg.id
}

output "alb_dns_name" {
  description = "The DNS name of the load balancer"
  value       = aws_lb.fastapi_alb.dns_name
}

output "alb_target_group_arn" {
  description = "The ARN of the target group"
  value       = aws_lb_target_group.fastapi_tg.arn
}
