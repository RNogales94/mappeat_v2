#!/bin/bash
#script para instalar las dependencias
npm init --force
npm i -S react react-dom
npm i -SD webpack webpack-dev-server
npm i -SD babel-loader babel-preset-es2015 babel-preset-react babel-core
mkdir app
mkdir app/components
mkdir public
