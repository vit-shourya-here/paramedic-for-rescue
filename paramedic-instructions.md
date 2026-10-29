Kubernetes CI/CD Practical — Assessment Runbook
Generic Python Application (GitHub Actions + Docker + Kubernetes)
This guide contains the terminal commands and the order of operations for the practical assessment. It provides the procedural execution steps required to build, test, and deploy the application container to a local Kubernetes environment.Important: Run all commands from the project root directory unless specified otherwise. Replace placeholders such as <GITHUB_REPO_URL> and <DOCKERHUB_USERNAME> with your actual deployment credentials. Never expose or commit plain-text Docker Hub access tokens.
1. Open the project folder
Open PowerShell and navigate to the target project directory:

cd "$HOME\OneDrive\Desktop\AgilePractice"

Verify that all essential workspace artifacts are present:l
Get-ChildItem


Expected project structure:
* `app.py`
* `test_app.py`
* `requirements.txt`
* `Dockerfile`
* `deployment.yaml`
* `service.yaml`
* `.github\workflows\pipeline.yml`

*Note: If hidden files are suppressed, ensure hidden item visibility is enabled to confirm `.github\workflows\pipeline.yml`.*

## 2. Check the required tools

Verify that all required environment runtimes and CLI tools are installed and accessible in your path:

```powershell
python --version
python -m pip --version
git --version
docker --version
kubectl version --client

Initialize Docker Desktop and verify that the integrated Kubernetes single-node cluster is enabled and running.

Validate the active Kubernetes context:

kubectl config current-context
kubectl get nodes

Expected output: Active context should set to docker-desktop with the node status reporting Ready.
3. Install Python dependencies and test the application locally
Install project dependencies and execute the unit test suite locally:

python -m pip install -r requirements.txt
python -m pytest -v

Do not proceed until all unit tests pass without errors.

(Optional) Launch the local development server:

python app.py

Access http://localhost:5000 in your browser. Terminate the process using Ctrl+C before proceeding.
4. Configure Git (first-time setup only)
Configure global commit attribution if not previously set:

git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

If the repository is initialized, inspect the working tree and configured remotes:

git status
git remote -v
git branch

If Git has not been initialized in this folder, execute:l
git init
git branch -M main
git remote add origin <GITHUB_REPO_URL>


If the `origin` remote is already defined, update its address using:

```powershell
git remote set-url origin <GITHUB_REPO_URL>
5. Configure the GitHub Actions self-hosted runner
This pipeline relies on a self-hosted Windows runner to interact directly with the local Docker Desktop Kubernetes instance.

Navigate to your GitHub repository in a browser.
Go to Settings → Actions → Runners → New self-hosted runner.
Select Windows as the target platform and follow the download/configuration instructions provided by GitHub.
Accept the default runner configuration and labels unless specialized tags are defined in your workflow.
In PowerShell, open the runner directory and start the service process:

.\run.cmd

Maintain this runner console window active throughout the assessment. Closing the process will cause queued jobs to stall.
6. Configure Docker Hub credentials as GitHub repository secrets
Generate a Personal Access Token (PAT) with read/write privileges in Docker Hub. Then, configure repository secrets under Settings → Secrets and variables → Actions → New repository secret:

DOCKERHUB_USERNAME — Your Docker Hub account handle
DOCKERHUB_TOKEN — Your generated Docker Hub Access Token

Security requirement: Secrets must remain stored in GitHub settings and omitted from pipeline.yml, source code, or repository history.
7. Push 1 — first application version
Implement the initial feature set assigned for Push 1.

Validate source files and execute the local test suite:l
python -m pytest -v
git status


Stage required repository files and issue the baseline commit:

```powershell
git add app.py test_app.py requirements.txt Dockerfile deployment.yaml service.yaml .github/workflows/pipeline.yml
git commit -m "Push 1: Implement initial required features"
git push -u origin main
Verify Push 1
Open the repository's Actions tab on GitHub and inspect the triggered pipeline run.
Confirm successful execution across all stages: checkout, dependency resolution, testing, image build, registry push, and cluster deployment.
Check Docker Hub to verify the generation of the initial container image tag (matching the specific GitHub Actions run number).
8. Push 2 — updated application version
Incorporate the secondary feature requirements specified for Push 2. Update unit tests in test_app.py to cover new code paths.

Run local regression tests prior to committing:

python -m pytest -v
git status

Commit and push the secondary application revision:

git add app.py test_app.py requirements.txt Dockerfile deployment.yaml service.yaml .github/workflows/pipeline.yml
git commit -m "Push 2: Add remaining features for final assessment"
git push origin main

The push triggers a secondary execution run. The pipeline will compile a new, uniquely tagged Docker image and perform a rolling update on the target Kubernetes Deployment.

Note: Limit application updates to exactly two functional pushes per assessment guidelines. Non-application workflow fixes should adhere to assessor guidelines.
9. Check the GitHub Actions result
In GitHub:

Navigate to the Actions tab.
Select the pipeline execution corresponding to the latest commit.
Confirm that all step indicators display green completion states.
If failures occur, expand the relevant step log, diagnose root causes, apply remediation locally, and re-push as permitted.

Ensure the self-hosted runner console remains online throughout job execution.
10. Verify Docker images
Open Docker Hub in a browser to confirm the existence of two distinct image tags, corresponding to each respective workflow run.

Verify local images via PowerShell:

docker images

To inspect specific image metadata, execute:l
docker image inspect <DOCKERHUB_USERNAME>/web-app:


*Ensure the tag assigned to the live Kubernetes Deployment corresponds to the latest image built by the runner.*

## 11. Verify Kubernetes deployment and service

Query active cluster resources:

```powershell
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get endpoints app-service

Verify the image tag actively referenced by the Deployment manifest:

kubectl get deployment app-deployment -o jsonpath="{.spec.template.spec.containers[0].image}"

Check the rollout status of the Deployment:

kubectl rollout status deployment/app-deployment --timeout=120s
Success Criteria Indicators
Deployment: Reports 1/1 ready replicas.
Pods: Status displays Running and ready.
Services: app-service is active with valid endpoint bindings.
Image: Live container references the tag built during the final pipeline run.

Troubleshooting non-ready Pod states:

kubectl describe deployment app-deployment
kubectl describe pod <POD_NAME>
kubectl logs deployment/app-deployment
12. Open the deployed application
While the service exposes NodePort 30090, local network virtualization on Docker Desktop may restrict direct access. Establish a local proxy via port-forwarding:

Run in a dedicated PowerShell terminal:

kubectl port-forward service/app-service 5001:5000

Access the live application at: http://localhost:5001

Maintain the port-forward process active during demonstration. Restart the command if network connections drop following new deployments.
13. Useful troubleshooting commands
# Inspect cluster status and event logs
kubectl get all
kubectl get events --sort-by=.metadata.creationTimestamp

# Detailed pod diagnostics and stdout logs
kubectl get pods -o wide
kubectl logs deployment/app-deployment

# Network service and endpoint binding details
kubectl describe service app-service
kubectl get endpoints app-service

# Context and node health verification
kubectl config current-context
kubectl get nodes
14. Assessment Evidence Checklist
Prepare clear screenshots covering the following items:

Directory layout in VS Code / File Explorer displaying required project artifacts.
Successful completion log for Push 1 workflow execution.
Successful completion log for Push 2 workflow execution.
Passing execution logs from local pytest execution.
Docker Hub repository listing showing both unique image tags.
Terminal outputs for kubectl get deployments, kubectl get pods, and kubectl get services.
Web browser displaying the live application demonstrating Push 2 functionality.

Ensure all access tokens, keys, and private credentials are redacted prior to submission.
15. Summary Statement for Assessor
"I developed the application in Python. GitHub Actions checks out the source code, installs dependencies, and runs pytest. If the tests pass, the workflow builds a Docker image with a unique tag, pushes it to Docker Hub, and updates the Kubernetes Deployment to use that image. The application is exposed through a Kubernetes Service. Push 1 implemented the initial required functionality; Push 2 added the remaining assessment features."
