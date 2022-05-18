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
            info = wikipedia.summary(e.options[0], sentences=2, auto_suggest=False)
            logger.info('Redirected to %s'%e.options[0])
        except wikipedia.exceptions.PageError as e:
            info = 'Page not found on wiki'
        except Exception as e:
            info = 'Wiki errpr'
        explained_kws.append(kw + (info, ))
    return explained_kws
