#!/bin/sh

# Decrypt the file
mkdir ./secrets
# --batch to prevent interactive command --yes to assume "yes" for questions
gpg --batch --yes --decrypt --passphrase="$GOOGLE_PW" \
--output ./secrets/googleKeys_jpsullivan_ec500.json googleKeys_jpsullivan_ec500.json.gpg
