import apns

from twisted.internet import reactor

#deviceToken = 'b071e0ecebc859e60310f7671d7d1bd3dbc2b760ed258fbe3d76ec974ccd4e89'
#certFilePath = '/Users/unsouled/Project/node-APNS/package/test.pem'
#privFilePath = '/Users/unsouled/Project/node-APNS/package/test.pem'

deviceToken = '892635a97209b5867078dd778cdd5cddd9ec690be8c22f541d208121d7c6bb40'
certFilePath = '/home/unsouled/lumen/cert/lumen-example/cert.pem'
privFilePath = '/home/unsouled/lumen/cert/lumen-example/priv.pem'

apns.push(deviceToken, {'from':'Someone', 'body':'HI?!'}, certFilePath, privFilePath, 'development')

reactor.run()
