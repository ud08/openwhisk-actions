function action(params){
        return new Promise((resolve,reject)=>{
                var Client = require('ssh2').Client;
                var conn = new Client();
                conn.on('ready',()=>{
                        conn.exec('if [[ ! -e '+params.dirname+'  ]]; then mkdir '+params.dirname+'; fi',(err,stream)=>{
                                        if (err) {
                                                resolve({"result":"directory not created"});
                                        }else{
                                                stream
                                                .on('close',(code,signal)=>{
                                                        conn.end();
                                                })
                                                .on('data',(data)=>{
                                                        installedpackages.push("yum");
                                                })
                                                .stderr.on('data', (data) => {
                                                        console.log("error: "+data);
                                                });
                                        }
                        });
                        resolve({"resukt":"directory created"});
                })
                .connect({
                        host: params.hostname,
                        port: params.port,
                        username: params.username,
                        password: params.password
                });
        });
}
exports.main = action;
