FROM zhengxiaoyao0716/flask

MAINTAINER zhengxiaoyao0716

ADD .uwsgi.ini /web/
RUN mkdir /web/share/.log

# ENTRYPOINT ["uwsgi", "/web/.uwsgi.ini"]
CMD ["uwsgi", "/web/.uwsgi.ini"]
