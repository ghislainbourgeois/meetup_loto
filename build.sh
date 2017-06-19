docker network create --driver bridge meetup_loto_net
docker run -d -e 'ssl=true' --net=meetup_loto_net -v $(pwd)/tests/mock/meetup:/config -e 'custom_responses_config=/config/config.yml' --name api.meetup.com campanda/webserver-mock
docker build --build-arg TRAVIS_JOB_ID=${TRAVIS_JOB_ID} --network meetup_loto_net -t ghibourg/meetup_loto .
docker stop api.meetup.com
docker rm api.meetup.com
