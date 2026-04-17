pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        POSTGRES_USER = credentials('postgres-user')
        POSTGRES_PASSWORD = credentials('postgres-password')
        RABBITMQ_USER = credentials('rabbitmq-user')
        RABBITMQ_PASSWORD = credentials('rabbitmq-password')
        DATABASE_URL = credentials('database-url')
        SECRET_KEY = credentials('secret-key')
        POKEMON_API_URL = "https://pokeapi.co/api/v2"

        COMPOSE_PROJECT_NAME = "pokeDiary"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create .env') {
            steps {
                sh '''
        cat <<EOF > .env
        POSTGRES_USER=$POSTGRES_USER
        POSTGRES_PASSWORD=$POSTGRES_PASSWORD
        RABBITMQ_USER=$RABBITMQ_USER
        RABBITMQ_PASSWORD=$RABBITMQ_PASSWORD
        DATABASE_URL=$DATABASE_URL
        SECRET_KEY=$SECRET_KEY
        POKEMON_API_URL=$POKEMON_API_URL
        EOF
                '''
            }
        }

        stage('Build Containers') {
            steps {
                sh 'docker-compose build --no-cache'
            }
        }

        stage('Start Services') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Wait for Services') {
            steps {
                sh '''
                echo "Waiting for services up..."
                sleep 15
                docker-compose ps
                '''
            }
        }

        stage('Health Check API') {
            steps {
                sh '''
                echo "Testing API..."
                curl -f http://localhost:8000/docs || exit 1
                '''
            }
        }

        stage('Run Tests (!next step!)') {
            when {
                expression { return false }
            }
            steps {
                sh 'pytest'
            }
        }
    }

    post {
        success {
            echo 'Build success!'
        }

        failure {
            echo 'Error detected. Displaying logs...'
            sh 'docker-compose logs'
        }

        always {
            echo 'Finishing containers...'
            sh 'docker-compose down -v'
            sh 'rm -f .env'
        }
    }
}