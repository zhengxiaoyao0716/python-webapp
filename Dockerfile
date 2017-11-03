FROM zhengxiaoyao0716/flask

MAINTAINER zhengxiaoyao0716

ADD .uwsgi.ini /web/

CMD ["uwsgi", "/web/.uwsgi.ini"]
