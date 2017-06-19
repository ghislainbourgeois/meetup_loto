https=
if [ ${env} = "mock" ]; then
  export REQUESTS_CA_BUNDLE=""
  export CURL_CA_BUNDLE=""
fi
twistd -n web --wsgi server.app
