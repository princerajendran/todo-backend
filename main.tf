provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "todo_backend" {
  metadata {
    name = "todo-backend"
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "todo-backend"
      }
    }
    template {
      metadata {
        labels = {
          app = "todo-backend"
        }
      }
      spec {
        container {
          name  = "todo-backend"
          image = "princerajendran/todo-backend:1.0"
          port {
            container_port = 8080
          }
        }
      }
    }
  }
}