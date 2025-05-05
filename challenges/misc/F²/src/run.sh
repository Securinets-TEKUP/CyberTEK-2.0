#!/bin/bash

docker run -dit -p 31337:1337 -v ./travler-gate:/var/secrets/chxmxii/travler-gate -v ./travler-key:/var/secrets/chxmxii/travler-key -v ./travler-inv:/var/secrets/chxmxii/travler-inv -v ./travler-ep:/var/secrets/chxmxii/travler-ep chxmxi/travler:v1