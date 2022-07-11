/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    config = {
        "COUCH_URL": "",
        "IAM_API_KEY": ""
    }

    const authenticator = new IamAuthenticator({apikey: config.IAM_API_KEY})
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(config.COUCH_URL);
    if (params.state) {
        var selector = {"st": params.state};
        var result = await getMatchingRecords(cloudant, "dealerships", selector);
        return result;
    } else {
        var result = await getAllRecords(cloudant, "dealerships");
        format_result = [];
        for (var i = 0; i < result["result"].length; i++) {
            format_result.push(result["result"][i]["doc"]);
        }
        result = {"result": format_result};
        return result;
    }
}

function getMatchingRecords(cloudant, dbname, selector) {
    return new Promise((resolve, reject) => {
        cloudant.postFind({db: dbname, selector: selector})
            .then((result) => {
                resolve({result: result.result.docs});
            })
            .catch(err => {
                console.log(err);
                reject({err: err});
            });
    })
}

function getAllRecords(cloudant, dbname) {
    return new Promise((resolve, reject) => {
        cloudant.postAllDocs({db: dbname, includeDocs: true, limit: 10})
            .then((result) => {
                resolve({result: result.result.rows});
            })
            .catch(err => {
                console.log(err);
                reject({err: err});
            });
    })
}