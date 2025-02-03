// --- Copyright (c) 2024 Linagora
// licence       : GPL v3
// - Flavien Perez fperez@linagora.com
// - Maïlys Jara mjara@linagora.com

pipeline {
    agent {
        docker {
            image "${env.HARBOR_REGISTRY}/${env.PROJECT_NAME}/${env.IMAGE_CACHE}:${env.CACHE_TAG}"
            args "--env DOCKER_TLS_CERTDIR=${env.DOCKER_TLS_CERTDIR}"
        }
    }
    environment {
        PROJECT_PATH = './gitlab_monitor'
        PROJECT_NAME = 'gitlab-monitor'
        HARBOR_REGISTRY = 'docker-registry.linagora.com'
        IMAGE_CACHE = 'gitlab-monitor-dev'
        DOCKER_TLS_CERTDIR = '/certs'
        CACHE_TAG = '1.0.0-dev'
        CODE_SOURCE = './gitlab_monitor/'
        IMAGE_CACHE_DEPLOY = 'gitlab-monitor-deploy-cache'
    }
    stages {
        stage('Lint') {
            parallel {
                stage('Pylint') {
                    steps {
                        script {
                            sh '''
                                pylint --version
                                pylint --output-format=colorized ${CODE_SOURCE}/*
                            '''
                        }
                    }
                }
                stage('Black') {
                    steps {
                        script {
                            sh '''
                                black --version
                                black ${CODE_SOURCE}/* --check --diff
                            '''
                        }
                    }
                }
                stage('Isort') {
                    steps {
                        script {
                            sh '''
                                isort --version
                                isort ${CODE_SOURCE}/* --check-only
                            '''
                        }
                    }
                }
                stage('Pycln') {
                    steps {
                        script {
                            sh '''
                                pycln --version
                                pycln --check ${CODE_SOURCE}/*
                            '''
                        }
                    }
                }
                stage('Mypy') {
                    steps {
                        script {
                            sh '''
                                mypy --version
                                mypy ${CODE_SOURCE} --junit-xml report_mypy.xml
                            '''
                        }
                    }
                    post {
                        always {
                            junit 'report_mypy.xml'
                        }
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    sh '''
                        export PYTHONPATH=$PYTHONPATH:$(pwd)
                        pytest --cov=gitlab_monitor --cov-report=html --cov-report=xml --junitxml=pytest_results.xml tests/unit/*
                    '''
                }
            }
            post {
                always {
                    junit 'pytest_results.xml'
                    archiveArtifacts artifacts: 'coverage.xml, pytest_results.xml, htmlcov/**', allowEmptyArchive: true
                }
            }
        }
    }
}
