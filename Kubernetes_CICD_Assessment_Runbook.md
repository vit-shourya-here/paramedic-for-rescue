# Kubernetes CI/CD Practical --- Assessment Runbook

## Menu-Driven Calculator (Python + GitHub Actions + Docker + Kubernetes)

This guide contains the **terminal commands and the order of
operations** for the practical. It does **not** reproduce the contents
of the seven project files (`app.py`, `test_app.py`, `requirements.txt`,
`Dockerfile`, `deployment.yaml`, `service.yaml`, and `pipeline.yml`).

> **Important:** Run commands from the project folder unless a step says
> otherwise. Replace placeholders such as `<GITHUB_REPO_URL>` and
> `<DOCKERHUB_USERNAME>` with your own values. Never paste a Docker Hub
> access token into a terminal command or commit it to GitHub.

------------------------------------------------------------------------

## 1. Open the project folder

Open PowerShell and navigate to the project directory:

``` powershell
cd "$HOME\OneDrive\Desktop\AgilePractice"
```

Check that the seven project files are present:

``` powershell
Get-ChildItem
```

Expected files:

-   `app.py`
-   `test_app.py`
-   `requirements.txt`
-   `Dockerfile`
-   `deployment.yaml`
-   `service.yaml`
-   `.github\workflows\pipeline.yml`

If the workflow file is not visible in File Explorer, remember that it
is inside `.github\workflows\`.

## 2. Check the required tools

``` powershell
python --version
python -m pip --version
git --version
docker --version
kubectl version --client
```

Start **Docker Desktop** and make sure its Kubernetes cluster is enabled
and running.

Check Kubernetes:

``` powershell
kubectl config current-context
kubectl get nodes
```

For this setup, the context should normally be `docker-desktop`, and the
node should show `Ready`.

## 3. Install Python dependencies and test the application locally

``` powershell
python -m pip install -r requirements.txt
python -m pytest -v
```

Continue only when the tests pass. If tests fail, fix the issue before
pushing.

Optional: start the Flask app locally:

``` powershell
python app.py
```

Open `http://localhost:5000` in a browser. Stop the local server with
`Ctrl+C` before continuing if needed.

## 4. Configure Git (first-time setup only)

Set the identity that should appear on your commits:

``` powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

If the folder is already a Git repository, check its status and remote:

``` powershell
git status
git remote -v
git branch
```

If Git has **not** been initialized yet, run:

``` powershell
git init
git branch -M main
git remote add origin <GITHUB_REPO_URL>
```

If `origin` already exists, do not add it again. To correct its URL:

``` powershell
git remote set-url origin <GITHUB_REPO_URL>
```

## 5. Configure the GitHub Actions self-hosted runner

This project uses a **self-hosted Windows runner** so the workflow can
access the local Docker Desktop Kubernetes cluster.

1.  Open the GitHub repository in your browser.
2.  Go to **Settings → Actions → Runners → New self-hosted runner**.
3.  Select **Windows** and follow GitHub's current instructions to
    download and configure the runner.
4.  Configure it for the repository and leave the default runner labels
    unless your workflow specifies otherwise.
5.  In PowerShell, go to the downloaded runner directory and start it:

``` powershell
.\run.cmd
```

Keep this runner window open while the GitHub Actions workflow runs. Do
not close it during the assessment. If the runner is offline, the job
will remain queued or fail to start.

## 6. Configure Docker Hub credentials as GitHub repository secrets

In Docker Hub, create a Personal Access Token with the permissions
required to push images. Then, in the GitHub repository, open **Settings
→ Secrets and variables → Actions → New repository secret** and add:

-   `DOCKERHUB_USERNAME` --- your Docker Hub username
-   `DOCKERHUB_TOKEN` --- your Docker Hub access token

Use the token as a GitHub secret; do not put it in `pipeline.yml`,
Python files, or Git commits.

## 7. Push 1 --- first application version

For the first version, the calculator supports **addition and
subtraction**.

Check the files and run tests:

``` powershell
python -m pytest -v
git status
```

Stage the project files and make the first application-version commit:

``` powershell
git add app.py test_app.py requirements.txt Dockerfile deployment.yaml service.yaml .github/workflows/pipeline.yml
git commit -m "Push 1: Add addition and subtraction"
git push -u origin main
```

If the repository already tracks the files and the upstream is set,
`git push origin main` is sufficient.

### Verify Push 1

On GitHub, open **Actions** and select the workflow run triggered by
this push. Check that checkout, dependency installation, tests, Docker
build, Docker Hub push, and Kubernetes deployment all succeed.

Check Docker Hub and confirm that the first image tag exists. The
workflow uses the GitHub Actions run number as the image tag, so use the
actual tag shown in the successful run---not an assumed number.

## 8. Push 2 --- updated application version

Update the application to add **multiplication and division**. Keep the
test file updated to test the new features, including division by zero.

Run the tests before committing:

``` powershell
python -m pytest -v
git status
```

Commit and push the second application version:

``` powershell
git add app.py test_app.py requirements.txt Dockerfile deployment.yaml service.yaml .github/workflows/pipeline.yml
git commit -m "Push 2: Add multiplication and division"
git push origin main
```

The push should trigger a second workflow run. The pipeline should build
and push a **new, unique Docker image tag** and update the Kubernetes
Deployment to use that tag.

**Assessment note:** The brief requires exactly two application-version
pushes. Avoid making extra feature commits. If you need to fix a
workflow/configuration problem, follow your instructor's guidance on
whether such a fix counts as another push.

## 9. Check the GitHub Actions result

In GitHub:

1.  Open the repository's **Actions** tab.
2.  Open the run for the latest push.
3.  Confirm that every step has a green check.
4.  If a step fails, open that step's log, identify the error, fix it,
    rerun or push according to your assessment rules, and verify the
    result.

The runner terminal must be running during the job. Do not share
screenshots that reveal tokens or secret values.

## 10. Verify Docker images

Open your Docker Hub repository in a browser and check that **two
distinct tags** exist, one for each application-version push.

Optional local checks in PowerShell:

``` powershell
docker images
```

To inspect an image tag, replace the placeholders:

``` powershell
docker image inspect <DOCKERHUB_USERNAME>/calculator:<TAG>
```

The image tag used by the Kubernetes Deployment must match the tag built
and pushed by that workflow run.

## 11. Verify Kubernetes deployment and service

Run:

``` powershell
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get endpoints calculator-service
```

Check the image currently used by the calculator Deployment:

``` powershell
kubectl get deployment calculator -o jsonpath="{.spec.template.spec.containers[0].image}"
```

Check rollout status:

``` powershell
kubectl rollout status deployment/calculator --timeout=120s
```

Expected signs of success:

-   Deployment shows `1/1` available (for a one-replica deployment).
-   Calculator Pod is `Running` and ready.
-   `calculator-service` exists.
-   The service has a non-empty endpoint.
-   The deployed image uses the tag for the latest successful
    application push.

If the Pod is not ready, inspect it:

``` powershell
kubectl describe deployment calculator
kubectl describe pod <POD_NAME>
kubectl logs deployment/calculator
```

Replace `<POD_NAME>` with the actual Pod name shown by
`kubectl get pods`.

## 12. Open the deployed application

The service is configured with NodePort `30090`, but on some local
Docker Desktop setups `http://localhost:30090` may not respond. Use
port-forwarding if required.

Run this in a separate PowerShell window:

``` powershell
kubectl port-forward service/calculator-service 5001:5000
```

Keep that terminal open and visit:

`http://localhost:5001`

Submit sample calculations to demonstrate the updated version. The
port-forward command must remain running while you use the browser.

If the page stops responding after a new deployment, stop the old
port-forward with `Ctrl+C` and run the command again.

## 13. Useful troubleshooting commands

``` powershell
# Check Kubernetes resources
kubectl get all
kubectl get events --sort-by=.metadata.creationTimestamp

# Check the calculator Pod and logs
kubectl get pods -o wide
kubectl logs deployment/calculator

# Check the service and its endpoints
kubectl describe service calculator-service
kubectl get endpoints calculator-service

# Check Docker Desktop Kubernetes context
kubectl config current-context
kubectl get nodes
```

If Docker commands fail, check that Docker Desktop is open and the
Docker engine is running. If the GitHub Actions job is queued, check
that the self-hosted runner window is active and the runner is online in
GitHub.

## 14. Screenshots/evidence to prepare for assessment

Capture clear screenshots of:

-   [ ] Project files in VS Code / Explorer (show the required file
    names).
-   [ ] Successful first GitHub Actions run.
-   [ ] Successful second GitHub Actions run.
-   [ ] Pytest results showing all tests passed.
-   [ ] Docker Hub repository showing both unique image tags.
-   [ ] `kubectl get deployments`, `kubectl get pods`, and
    `kubectl get services`.
-   [ ] The deployed calculator running in the browser with
    multiplication and division available.

Do not include access tokens, passwords, or secret values in
screenshots.

## 15. Short explanation for the assessor

> "I developed the calculator in Python. GitHub Actions checks out the
> source code, installs dependencies, and runs pytest. If the tests
> pass, the workflow builds a Docker image with a unique tag, pushes it
> to Docker Hub, and updates the Kubernetes Deployment to use that
> image. The application is exposed through a Kubernetes Service. Push 1
> implemented addition and subtraction; Push 2 added multiplication and
> division."

**Remember:** The supplied practical brief specifies GitHub Actions.
Jenkins is not required by that brief unless your instructor separately
asks for it.
