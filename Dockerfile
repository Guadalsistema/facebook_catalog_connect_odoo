FROM odoo:13

USER root

RUN python3 -m pip install ipython ipdb
RUN apt update && apt install -y vim

USER odoo

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]