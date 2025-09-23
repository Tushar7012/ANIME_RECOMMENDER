# LLMOps Application Deployment Guide

This guide provides step-by-step instructions to deploy a containerized application on a Google Cloud VM using Docker, Minikube, and Kubernetes. It also includes steps for setting up monitoring with Grafana Cloud.

---

## 1. Prerequisites

Before you begin, ensure you have the following:
- A GitHub repository containing your application code.
- A `Dockerfile` in the root of your project.
- A Kubernetes deployment file named `llmops-k8s.yaml`.

---

## 2. Google Cloud VM Setup

1.  **Create a VM Instance**
    - Go to the Google Cloud Console and navigate to **VM Instances**.
    - Click **"Create Instance"** with the following configuration:
        - **Series**: `E2`
        - **Machine Type**: `Standard` with `16 GB RAM`
        - **Boot Disk**: Image: `Ubuntu 24.04 LTS`, Size: `256 GB`
        - **Firewall**: Enable **Allow HTTP traffic** and **Allow HTTPS traffic**.
    - Create the instance.

2.  **Connect to the VM**
    - Once the instance is running, connect to it using the **SSH** option provided in the Google Cloud console.

---

## 3. Configure the VM Environment

1.  **Clone Your GitHub Repository**
    ```bash
    git clone [https://github.com/data-guru0/TESTING-9.git](https://github.com/data-guru0/TESTING-9.git)
    cd TESTING-9
    ```

2.  **Install Docker**
    - Follow the official instructions on the Docker website to install Docker on Ubuntu.
    - Test the installation:
      ```bash
      docker run hello-world
      ```
    - Follow the "Post-installation steps for Linux" on the same page to run Docker without `sudo`.
    - Configure Docker to start on boot:
      ```bash
      sudo systemctl enable docker.service
      sudo systemctl enable containerd.service
      ```
    - Verify that Docker is active:
      ```bash
      systemctl status docker
      ```

3.  **Install Minikube and kubectl**
    - Install the Minikube binary by following the official instructions for Linux (x86 architecture).
    - Start the Minikube cluster:
      ```bash
      minikube start
      ```
    - Install `kubectl` using snap:
      ```bash
      sudo snap install kubectl --classic
      ```
    - Verify your cluster status:
      ```bash
      minikube status
      kubectl get nodes
      ```

---

## 4. Build and Deploy Your Application

1.  **Point Docker to the Minikube Environment**
    ```bash
    eval $(minikube docker-env)
    ```

2.  **Build the Docker Image**
    ```bash
    docker build -t llmops-app:latest .
    ```

3.  **Create Kubernetes Secrets**
    *Note: Replace the empty strings with your actual API keys.*
    ```bash
    kubectl create secret generic llmops-secrets \
      --from-literal=GROQ_API_KEY="YOUR_GROQ_API_KEY" \
      --from-literal=HUGGINGFACEHUB_API_TOKEN="YOUR_HUGGINGFACE_TOKEN"
    ```

4.  **Deploy the Application**
    ```bash
    kubectl apply -f llmops-k8s.yaml
    kubectl get pods
    ```

5.  **Expose and Access Your Application**
    - **In a new terminal**, start the Minikube tunnel. Keep this terminal open.
      ```bash
      minikube tunnel
      ```
    - **In a third terminal**, forward the service port:
      ```bash
      kubectl port-forward svc/llmops-service 8501:80 --address 0.0.0.0
      ```
    - You can now access your app at `http://<YOUR_VM_EXTERNAL_IP>:8501`.

---

## 5. Set Up Grafana Cloud Monitoring

1.  **Create a Monitoring Namespace**
    ```bash
    kubectl create ns monitoring
    ```

2.  **Install Helm**
    - Follow the official documentation to install Helm on your VM.

3.  **Configure Grafana Cloud Kubernetes Integration**
    - In your Grafana Cloud account, go to **Observability -> Kubernetes** and start the integration setup.
    - Provide a **Cluster Name** (`minikube`) and **Namespace** (`monitoring`).
    - Create and save a new access token.
    - Grafana will generate a Helm command and YAML configuration.

4.  **Deploy the Grafana Agent**
    - Create a file to store the Grafana configuration:
      ```bash
      vi values.yaml
      ```
    - Paste the YAML content provided by Grafana into this file. Save and close it (`Esc` + `:wq!`).
    - Modify the `helm upgrade` command provided by Grafana to use your file:
      ```bash
      helm repo add grafana [https://grafana.github.io/helm-charts](https://grafana.github.io/helm-charts) && \
      helm repo update && \
      helm upgrade --install --atomic --timeout 300s grafana-k8s-monitoring grafana/k8s-monitoring \
        --namespace "monitoring" --create-namespace --values values.yaml
      ```
    - Run the modified command in your VM.

5.  **Verify Monitoring**
    - Check that the Grafana agent pods are running:
      ```bash
      kubectl get pods -n monitoring
      ```
    - Return to the Grafana Cloud dashboard to view your cluster metrics.

---

## 6. Git Configuration

To push code changes from the VM back to GitHub, configure your Git identity.

```bash
git config --global user.email "gyrogodnon@gmail.com"
git config --global user.name "data-guru0"