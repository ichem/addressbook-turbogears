# -*- coding: utf-8 -*-
"""Setup the rubrica application"""
from __future__ import print_function, unicode_literals
import transaction
from rubrica import model


def bootstrap(command, conf, vars):
    """Place any commands to setup rubrica here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = 'manager'
        u.display_name = 'Example manager'
        u.email_address = 'manager@somedomain.com'
        u.password = 'managepass'

        model.DBSession.add(u)

        g = model.Group()
        g.group_name = 'managers'
        g.display_name = 'Managers Group'

        g.users.append(u)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = 'manage'
        p.description = 'This permission gives an administrative right'
        p.groups.append(g)

        model.DBSession.add(p)

        u1 = model.User()
        u1.user_name = 'editor'
        u1.display_name = 'Example editor'
        u1.email_address = 'editor@somedomain.com'
        u1.password = 'editpass'

        rubrica = [   #inizializzo rubrica con 3 contatti
            ('Dario','3598761023',u),
            ('Piero','3289674102',u),
            ('Marta','3339748103',u)
        ]
        for nome, contatto, utente in rubrica:
            c = model.Contatto(name=nome,phone=contatto)
            utente.contacts.append(c) 
            model.DBSession.add(c)
        

        model.DBSession.add(u1)
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
