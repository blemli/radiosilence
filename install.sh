sudo apt install uhubctl git python3-pip
cp motd /etc/motd
sudo cp -f radiosilence.service /lib/systemd/system/radiosilence.service
sudo chmod 644 /lib/systemd/system/radiosilence.service
sudo systemctl daemon-reload
sudo systemctl enable radiosilence.service