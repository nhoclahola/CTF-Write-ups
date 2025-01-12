FROM php:7.2-apache
RUN docker-php-ext-install mysqli pdo pdo_mysql
WORKDIR /var/www/html/
COPY ./src /var/www/html/
COPY ./flag.txt /var/www/html/flag.txt
RUN echo "<Files \"flag.txt\">\n    Require all denied\n</Files>" > /var/www/html/.htaccess
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 750 /var/www/html \
    && chmod 640 /var/www/html/flag.txt
