pipeline {
    agent any
    stages {
        stage('Get Input Parameter'){
            steps {
                script {
                    getInputParam()
                    //cloneTfModules()
                    //props = getPipelineProps()
                }
            }
        }

        stage('Get AWS Creds') {
            steps{
                awsLogin('442203920185')
            }
        }
    }
}
