#!/bin/bash
datum="2022-12-15_120135.tar.gz"
rclone -v copy ./data/$datum fgdrive:/
