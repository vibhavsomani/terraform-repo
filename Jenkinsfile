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
                sh 'aws configure set aws_access_key_id AKIAWN5LIK446EHCVX3C'
                sh 'aws configure set aws_secret_access_key 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'
                sh 'aws configure set default.region us-east-1'
            }
  
        }
        
//Get the dynamic inputs from Python Boto3
        stage('Get Dynamic Inputs'){
            steps{
                script{
                    timeout(time: 10, unit: 'MINUTES'){
                        get_dynamic_inputs()
                    }
                }
            }
        }

//dynamically create tfvars
//         stage('Create Tfvars File'){
//             steps{
//                 script{
//                     createTfvarsFile()
//                 }
//             }
//         }
            
//Create Terraform init
//         stage('TerraformInit') {
//             steps{
//                 script{
//                     terraformInit()
//                 }
//             }
//         }
// //Create Terraform plan
//         stage('TerraformPlan'){
//             steps{
//                 sh '''
//                     terraform validate
//                     terraform plan
//                 '''
//             }
//         }

// //Apply the Terraform configuration based on the plan after approval
//         stage('TerraformApply'){
//             steps{
//                 script{
//                     runTerraformApply()
//                 }
//             }
//         }
//     }
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

def get_dynamic_inputs(){
    env.all_vpc_name = selectValue("vpc" , region , '' , '')
}

def getInputParam(){
    properties([
        parameters([
            string(description: 'Enter the account number', name: 'account_number', defaultValue: '442203920185')
        ])
    ])
}
