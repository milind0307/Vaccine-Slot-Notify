var AWS = require("aws-sdk");
AWS.config.update({ region: 'ap-south-1' }); //Region of Cognito Federated ID
var cognitoidentity = new AWS.CognitoIdentity();
var params = {
    IdentityPoolId: 'ap-south-1:a9f11227-8859-4fd8-b26a-5e84417370c7', /* required */
    AccountId: '367382347'
};
cognitoidentity.getId(params, function (err, data) {
    if (err) console.log(err, err.stack); // an error occurred
    else {
        //console.log(data);
        if (data.IdentityId != null) {
            cognitoidentity.getOpenIdToken(data, function (err, data2) {
                if (err) console.log(err, err.stack); // an error occurred
                else {
                    var params = {
                        DurationSeconds: 1800,
                        RoleArn: "arn:aws:iam::367382347:role/cognito-web-auth-role",
                        RoleSessionName: "Token",
                        WebIdentityToken: data2.Token.toString()
                    };
                    var sts = new AWS.STS({ apiVersion: '2011-06-15' });
                    sts.assumeRoleWithWebIdentity(params, function (err, data3) {
                        if (err) console.log(err, err.stack); // an error occurred
                        else {
                            //console.log(data3.Credentials.AccessKeyId);
                            //console.log(data3.Credentials.SecretAccessKey);
                            //console.log(data3.Credentials.SessionToken);

                            var cognitoidentityserviceprovider = new AWS.CognitoIdentityServiceProvider(options = {
                                accessKeyId: data3.Credentials.AccessKeyId.toString(),
                                secretAccessKey: data3.Credentials.SecretAccessKey.toString(),
                                sessionToken: data3.Credentials.SessionToken.toString()
                            });
                            var params = {
                                AuthFlow: 'ADMIN_NO_SRP_AUTH', /* required */
                                ClientId: '2orjga8tk9nj17rl5g', /* required */
                                UserPoolId: 'ap-south-1_p', /* required */
                                AuthParameters: {
                                    'USERNAME': 'antest',
                                    'PASSWORD': 'An@123'
                                    /* '<StringType>': ... */
                                }
                            };
                            cognitoidentityserviceprovider.adminInitiateAuth(params, function (err, data) {
                                if (err) console.log(err, err.stack); // an error occurred
                                else
                                {
                                    console.log(data.AuthenticationResult.IdToken);
                                    console.log(data.AuthenticationResult.ExpiresIn);
                                } 
                            });
                            
                        }
                    });
                }
            });
        }
    }
});
