node{
    dir("testtask"){
    try {
        def tests_successful = false
        stage('Preparation') {
                //git clone
                sh "sudo docker build . -t test_task"
                sh "$ rm -rf tmp/*"
                sh "mkdir -p tmp/ci_artifacts"
        }

        stage("Running tests"){

            tests_successful = sh (script: "sudo docker run -v $(pwd)/tmp/:/tests/tmp -it test_task python3.7 -m pytest --junit-xml=tmp/ci_artifacts/junit.xml -m functional", returnStatus: true) == 0
        }
        stage("Archiving artifacts"){
            allure includeProperties: false, jdk: '', properties: [[key: '', value: '']], results: [[path: 'tmp/ci-reports/']]
            junit allowEmptyResults: true, keepLongStdio: true, testResults: 'tmp/ci_artifacts/junit.xml'
            archiveArtifacts artifacts: 'tmp/logs/**', fingerprint: true
        }

    } catch (e) {
        // If there was an exception thrown, the build failed
        currentBuild.result = "FAILED"
        throw e
      } finally {
        // Finalization code
      }
    }
}