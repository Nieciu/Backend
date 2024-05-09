pipeline {
    agent any
    environment {
        ENV_FILE = credentials('backend-dep-sec')
        SERVER_IP = credentials('backend-ip')
    }

    stages {
        stage('Clone repository') {
            steps {
                echo 'Cloning'
                sh 'rm -rf Backend'
                sh 'git clone https://github.com/Nieciu/Backend.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building...'
                sh 'docker build -t django-eurovision ./Backend'
            }
        }

        stage('Destroy Test') {
            steps {
                echo 'Destroying test...'
                sh 'docker rm django-eurovision-test'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'docker run -p 8000:8000 --env-file ${ENV_FILE} --name django-eurovision-test django-eurovision python manage.py test'
            }
        }

        stage('Pack Build') {
            steps {
                echo 'Packing...'
                sh 'docker save -o backend.tar django-eurovision'
            }
        }

        stage('Copy Docker Image to remote host') {
            steps {
                echo 'Copying...'
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'backend', keyFileVariable: 'keyFile', passphraseVariable: 'pass', usernameVariable: 'username')]) {
                        def remote = [name:'backend', host: SERVER_IP, user: username, identityFile: keyFile, allowAnyHosts: true]
                        sshPut remote: remote, from: 'backend.tar', into: '/home/ubuntu'
                        sshCommand remote: remote, command: 'free -h'
                    }
                }
            }
        }
        stage('Delete Container') {
            steps {
                echo 'Deleting...'
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'backend', keyFileVariable: 'keyFile', passphraseVariable: 'pass', usernameVariable: 'username')]) {
                        def remote = [name:'backend', host: SERVER_IP, user: username, identityFile: keyFile, allowAnyHosts: true]
                        sshCommand remote: remote, command: 'docker rm -f django-eurovision'
                    }
                }
            }
        }
        stage('Load image') {
            steps {
                echo 'Loading...'
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'backend', keyFileVariable: 'keyFile', passphraseVariable: 'pass', usernameVariable: 'username')]) {
                        def remote = [name:'backend', host: SERVER_IP, user: username, identityFile: keyFile, allowAnyHosts: true]
                        sshCommand remote: remote, command: 'docker load --input backend.tar'
                    }
                }
            }
        }
        stage('Run image') {
            steps {
                echo 'Running...'
                sh'cat $ENV_FILE > .envir'
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'backend', keyFileVariable: 'keyFile', passphraseVariable: 'pass', usernameVariable: 'username')]) {
                        def remote = [name:'backend', host: SERVER_IP, user: username, identityFile: keyFile, allowAnyHosts: true]
                        sshPut remote: remote, from: '.envir', into: '/home/ubuntu'
                        sshCommand remote: remote, command: 'docker run -d -p 8000:8000 --env-file .envir --name django-eurovision django-eurovision'
                    }
                    sh 'rm .envir'
                }
            }
        }
    }
}
