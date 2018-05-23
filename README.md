# api.promoiq.website
promoiq.website backend

## SSH into Webserver

```ssh -i web_server_key_pair.pem ubuntu@ec2-18-207-106-158.compute-1.amazonaws.com```

## Restart uWSGI Server

sudo systemctl status promoiq
sudo systemctl status promoiq |  sed -n 's/.*Main PID: \(.*\)$/\1/g p' | cut -f1 -d' ' | xargs kill -HUP
sudo systemctl daemon-reload
