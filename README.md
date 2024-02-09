This is a pretend application that receives homework submissions via a `POST` request, runs some tests, and logs a result. It doesn't really do any of those things; the purpose of this repository is to demonstrate how to pull the contents of a private git repository and then expose them inside a container.

In response to an authenticated `POST` request to the `/submit` endpoint, the application will attempt to run a `run-tests.sh` script located in `$TEST_RUNNER_TESTS_PATH`.

There is an automated workflow in [`.github/workflows`](.github/workflows/) that builds a container image for the Python application included in this repository. That image is used by the [Deployment manifest](manifests/deployment.yaml) to run the application in Kubernetes/OpenShift.

## Requirements

- A private repository that contains a `run-tests.sh` script.
- Credentials that allow you to clone the private repository.

## Configuration

The application requires the following environment variables:

- `TEST_RUNNER_GITHUB_USERNAME` -- username for authenticationg to github
- `TEST_RUNNER_GITHUB_TOKEN` -- [pat] for authenticating to github
- `TEST_RUNNER_REPOSITORY_URL` -- repository containing the tests
- `TEST_RUNNER_TESTS_PATH` -- path at which tests are mounted in the service container
- `TEST_RUNNER_USERNAME` -- username required to submit to test runner
- `TEST_RUNNER_PASSWORD` -- password required to submit to test runner

[pat]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

In the [Kubernetes manifests](manifests/), these are set using the `test-runner-config` secret, which is populated from `manifests/test-runner.env`. In the `manifests` directory, copy `test-runner.env.sample` to `test-runner.env` and then edit it appropriately.

## Deploying the application

You can deploy the manifests into your current namespace by running:

```
kubectl apply -k manifests
```

If you want to see what the manifests look like -- including the generated Secret -- without deploying the, you can run:

```
kubectl kustomize manifests
```
