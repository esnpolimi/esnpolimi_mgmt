Get-Content .envs\.local\.postgres | ForEach-Object { if ($_ -match '^(.*)=(.*)$') { Set-Item -Path "env:\$($matches[1])" -Value $matches[2] } }
Get-Content .envs\.local\.django | ForEach-Object { if ($_ -match '^(.*)=(.*)$') { Set-Item -Path "env:\$($matches[1])" -Value $matches[2] } }
Get-Content .envs\.local\.django_vhost | ForEach-Object { if ($_ -match '^(.*)=(.*)$') { Set-Item -Path "env:\$($matches[1])" -Value $matches[2] } }
$env:DATABASE_URL = "postgres://$($env:POSTGRES_USER):$($env:POSTGRES_PASSWORD)@$($env:POSTGRES_HOST):$($env:POSTGRES_PORT)/$($env:POSTGRES_DB)"
Set-Item -Path "env:USE_DOCKER" -Value "yes"
$TRUST_DOWNSTREAM_PROXY=1
