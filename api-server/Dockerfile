FROM nginx/unit:1.26.1-python3.9

# Update root CA
RUN --mount=type=secret,id=extra-root-ca \
if [ -f /run/secrets/extra-root-ca ]; then \
    cp /run/secrets/extra-root-ca /usr/share/pki/ca-trust-source/anchors/extra-root-ca.crt; \
    update-ca-trust; \
fi

# Copy resources
COPY requirements.txt /requirements.txt
COPY nginx-unit-config.json /docker-entrypoint.d/
COPY --chown=unit:unit authdemo/ /python-packages/authdemo

# Install Python libraries
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY Authlib-1.0.0rc1-py2.py3-none-any.whl /Authlib-1.0.0rc1-py2.py3-none-any.whl
RUN pip3 install /Authlib-1.0.0rc1-py2.py3-none-any.whl