# radiosilence
enforce radio silence during phone calls

## install 
```bash
cd /opt
sudo mkdir radiosilence
sudo chown pi radiosilence
git clone https://github.com/blemli/radiosilence && cd radiosilence
chmod +x install.sh && ./install.sh
```

## usage
send a http get request to http://radiosilence.local/silent to mute the speaker or http://radiosilence.local/loud to unmute it.
