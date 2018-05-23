# api.promoiq.website
promoiq.website backend



## Helpful Commands

SSH into EC2 instance:

```ssh -i web_server_key_pair.pem ubuntu@ec2-18-207-106-158.compute-1.amazonaws.com```

View uWSGI status:

```sudo systemctl status promoiq```

Restart uWSGI server (to update app):

```sudo systemctl status promoiq |  sed -n 's/.*Main PID: \(.*\)$/\1/g p' | cut -f1 -d' ' | xargs kill -HUP```

Reload the systemd process:

```sudo systemctl daemon-reload```
