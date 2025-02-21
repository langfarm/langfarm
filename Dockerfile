FROM langfarm/python:3.11.11

ARG APP_HOME=/langfarm
RUN mkdir -p $APP_HOME

COPY packages $APP_HOME/packages
COPY apps $APP_HOME/apps
COPY docker/bin $APP_HOME/bin
COPY LICENSE $APP_HOME/
COPY README.md $APP_HOME/
COPY pyproject.toml $APP_HOME/
COPY uv.lock $APP_HOME/


WORKDIR $APP_HOME
RUN touch $APP_HOME/.env

RUN chmod +x ./bin/*.sh

# 安装依赖
RUN uv sync --no-dev --no-cache --frozen

RUN chown admin:admin -R $APP_HOME
USER admin

ENV PORT=3080

#运行时再选择什么服务启动
#ENTRYPOINT ["dumb-init", "--"]
#CMD["./bin/entrypoint.sh"]
