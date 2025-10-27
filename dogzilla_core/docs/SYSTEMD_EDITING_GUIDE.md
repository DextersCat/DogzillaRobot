# Safe SystemD Service Editing Workflow

## For /etc/systemd/system/amy.service

### Before Editing
1. Always create a timestamped backup:
   ```bash
   sudo cp /etc/systemd/system/amy.service /etc/systemd/system/amy.service.bak.$(date +%Y%m%d_%H%M%S)
   ```

### Editing Options

#### Option 1: Direct edit with sudoedit (Recommended)
```bash
sudo EDITOR=nano sudoedit /etc/systemd/system/amy.service
```

#### Option 2: Edit locally then move (VS Code friendly)
1. Edit in workspace: `/home/spencer/amy_core/amy.service.tmp`
2. Move to system location:
   ```bash
   sudo mv /home/spencer/amy_core/amy.service.tmp /etc/systemd/system/amy.service
   sudo chown root:root /etc/systemd/system/amy.service
   sudo chmod 644 /etc/systemd/system/amy.service
   ```

#### Option 3: Use sudo tee (Paste-friendly)
```bash
sudo tee /etc/systemd/system/amy.service > /dev/null <<'EOF'
[Unit]
# ... paste content here ...
EOF
```

### After Editing
1. Reload systemd daemon: `sudo systemctl daemon-reload`
2. Restart service: `sudo systemctl restart amy.service`
3. Verify status: `sudo systemctl status amy.service --no-pager -l`
4. Check logs: `sudo journalctl -u amy.service -n 50 --no-pager`

### Backup Location
Backups are stored as: `/etc/systemd/system/amy.service.bak.YYYYMMDD_HHMMSS`

To restore a backup:
```bash
sudo cp /etc/systemd/system/amy.service.bak.20251024_130225 /etc/systemd/system/amy.service
sudo systemctl daemon-reload
sudo systemctl restart amy.service
```