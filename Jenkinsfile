pipeline {
    agent any
    stages {
        stage('Get Input Parameter'){
            steps {
                script {
                    //getInputParam()
                    //cloneTfModules()
                    props = getPipelineProps()
                }
            }
        }

        stage('Get AWS Creds') {
            steps{
                awsLogin('442203920185')
            }
  
        }

//Create Terraform init
        stage('TerraformInit') {
            steps{
                script{
                    terraformInit()
                }
            }
        }
//Create Terraform plan
        stage('TerraformPlan'){
            steps{
                sh '''
                    terraform validate
                    terraform plan
                '''
            }
        }

//Apply the Terraform configuration based on the plan after approval
        stage('TerraformApply'){
            steps{
                script{
                    runTerraformApply()
                }
            }
        }
    }
}

//Initialize Terraform
def terraformInit(){
    sh '''
        cat terraform.tfvars
        terraform init -upgrade
        terraform fmt
    '''
}

def runTerraformApply(){
    timeout(time: 10, unit: 'MINUTES'){
        def proceed = input(id: 'proceed', message: 'Do you wish to proceed.',
        parameters: [[$class: 'ChoiceParameterDefinition',defaultValue: 'strDef',
        description: 'describing choices', name: 'nameChoice', choices: "Yes"]
        ])
    }
    sh '''
        terraform apply -auto-approve=true -lock=false
    '''
}
