import wikipedia
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def getIntroFromWiki(kws):
    explained_kws = []
    for kw in kws:
        try:
            info = wikipedia.summary(kw[0], sentences=2, auto_suggest=False)
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                info = wikipedia.summary(e.options[1], sentences=2, auto_suggest=False)
                info += ' (First disambiguation option selected)'
                logger.info('Redirected to %s'%e.options[1])
            except Exception as e:
                info = 'No disambiguation options available'
        except wikipedia.exceptions.PageError as e:
            info = 'Page not found on wiki'
        except Exception as e3:
            info = 'Wiki error'
        explained_kws.append(kw + (info, ))
    return explained_kws

print(getIntroFromWiki([("specific", 'nn')]))