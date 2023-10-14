# radiosilence
enforce radio silence during phone calls

## install 
```bash
mkdir /opt/radiosilence
chown pi /opt/radiosilence
cd /opt/radiosilence
git clone https://github.com/blemli/radiosilence && cd radiosilence
chmod +x install.sh && ./install.sh
```

## usage
send a http get request to http://radiosilence.local/silent to mute the speaker or http://radiosilence.local/loud to unmute it.
