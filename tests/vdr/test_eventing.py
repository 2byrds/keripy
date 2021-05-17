import pytest

from keri.base import keeping, directing
from keri.core.coring import Versify, Serials, Ilks, MtrDex, Prefixer, Serder, Signer
from keri.core.eventing import TraitDex, SealEvent
from keri.db import dbing
from keri.db.dbing import snKey, dgKey
from keri.vdr import eventing, viring
from keri.kering import Version, EmptyMaterialError, DerivationError, MissingAnchorError, ValidationError, \
    MissingWitnessSignatureError
from keri.vdr.eventing import rotate, issue, revoke, backerIssue, backerRevoke, Tever


def test_incept():
    """
    Test incept utility function
    """

    pre = "DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM"
    bak1 = "EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc"
    bak2 = "DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU"
    bak3 = "Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"

    # no backers, allowed to add later
    serder = eventing.incept(pre, baks=[], code=MtrDex.Blake3_256)
    assert serder.raw == (
        b'{"v":"KERI10JSON0000a9_","i":"EiLMklo_OJmbv8D58wPlv_fudfEzuqsIl3mFYq640Jzg",'
        b'"ii":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"0","t":"vcp","c":[],"bt":"0","b":[]}')

    # no backers allowed
    serder = eventing.incept(pre, baks=[], cnfg=[TraitDex.NoBackers], code=MtrDex.Blake3_256)
    assert serder.raw == (
        b'{"v":"KERI10JSON0000ad_","i":"EjD_sFljMHXJCC3rEFL93MwHNGguKdC11mcMuQnZitcs",'
        b'"ii":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"0","t":"vcp","c":["NB"],"bt":"0","b":[]}')

    # no backers allows, one attempted
    with pytest.raises(ValueError):
        eventing.incept(pre, cnfg=[TraitDex.NoBackers],
                        baks=[bak1])

    # with backer dupes
    with pytest.raises(ValueError):
        eventing.incept(pre, cnfg=[],
                        baks=[bak1, bak1, bak2])

    # with oob toad
    with pytest.raises(ValueError):
        eventing.incept(pre, cnfg=[], toad=4,
                        baks=[bak1, bak2, bak3])

    # with oob toad
    with pytest.raises(ValueError):
        eventing.incept(pre, cnfg=[], toad=1,
                        baks=[])

    # one backer
    serder = eventing.incept(pre,
                             baks=[bak1],
                             code=MtrDex.Blake3_256)
    assert serder.raw == (
        b'{"v":"KERI10JSON0000d7_","i":"EVohdnN33-vdNOTPYxeTQIWVzRKtzZzBoiBSGYSSnD0s",'
        b'"ii":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"0","t":"vcp","c":[],"bt":"1",'
        b'"b":["EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc"]}')

    # 3 backers
    serder = eventing.incept(pre,
                             baks=[bak1, bak2, bak3],
                             code=MtrDex.Blake3_256)
    assert serder.raw == (
        b'{"v":"KERI10JSON000135_","i":"Ez5ncVo7zXjC9DJT8-DM-ZMqJ-WtgpEGGs8JUzXh_Tc0",'
        b'"ii":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"0","t":"vcp","c":[],"bt":"3",'
        b'"b":["EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc","DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU",'
        b'"Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"]}')

    # one backer, with threshold
    serder = eventing.incept(pre,
                             toad=1,
                             baks=[bak1],
                             code=MtrDex.Blake3_256)
    assert serder.raw == (
        b'{"v":"KERI10JSON0000d7_","i":"EVohdnN33-vdNOTPYxeTQIWVzRKtzZzBoiBSGYSSnD0s",'
        b'"ii":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"0","t":"vcp","c":[],"bt":"1",'
        b'"b":["EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc"]}')

    # 3 backers, with threshold
    serder = eventing.incept(pre,
                             toad=2,
                             baks=[bak1, bak2, bak3],
                             code=MtrDex.Blake3_256)
    assert serder.raw == (
        b'{"v":"KERI10JSON000135_","i":"E39gu2hSUBannC3st40r2d8Dy7T6JsyTk0JefYYPtDgE",'
        b'"ii":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"0","t":"vcp","c":[],"bt":"2",'
        b'"b":["EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc","DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU",'
        b'"Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"]}')

    """ End Test """


def test_rotate():
    """
    Test rotate functionality

    """
    dig = "EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg"
    bak1 = "EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc"
    bak2 = "DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU"
    bak3 = "Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"

    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    baks=[])
    assert serder.raw == (b'{"v":"KERI10JSON0000aa_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
                          b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"1","t":"vrt","bt":"0","br":[],'
                          b'"ba":[]}')

    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    sn=3,
                    baks=[bak1])
    assert serder.raw == (
        b'{"v":"KERI10JSON0000aa_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
        b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"3","t":"vrt","bt":"1","br":[],"ba":[]}')

    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    sn=4,
                    baks=[bak1, bak2, bak3])
    assert serder.raw == (
        b'{"v":"KERI10JSON0000aa_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
        b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"4","t":"vrt","bt":"3","br":[],"ba":[]}')

    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    sn=4,
                    baks=[bak1, bak2, bak3],
                    cuts=[bak2])
    assert serder.raw == (
        b'{"v":"KERI10JSON0000d8_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
        b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"4","t":"vrt","bt":"2",'
        b'"br":["DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU"],"ba":[]}')

    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    sn=4,
                    baks=[bak1, bak2, bak3],
                    cuts=[bak2, bak3])
    assert serder.raw == (
        b'{"v":"KERI10JSON000107_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
        b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"4","t":"vrt","bt":"1",'
        b'"br":["DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU","Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"],'
        b'"ba":[]}')

    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    sn=4,
                    baks=[bak1, bak2, bak3],
                    cuts=[bak1, bak2, bak3])
    assert serder.raw == (
        b'{"v":"KERI10JSON000136_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
        b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"4","t":"vrt","bt":"0",'
        b'"br":["EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc","DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU",'
        b'"Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"],"ba":[]}')

    # invalid cut
    with pytest.raises(ValueError):
        rotate(dig=dig,
               regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
               sn=4,
               baks=[bak1, bak3],
               cuts=[bak2])

    # invalid cut
    with pytest.raises(ValueError):
        rotate(dig=dig,
               regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
               sn=4,
               baks=[bak1, bak3],
               cuts=[bak2])

    # invalid toad
    with pytest.raises(ValueError):
        rotate(dig=dig,
               regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
               sn=4,
               toad=2,
               baks=[bak1, bak3],
               cuts=[bak3])

    # invalid sn
    with pytest.raises(ValueError):
        rotate(dig=dig,
               regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
               sn=0,
               baks=[])

    # adds
    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    sn=4,
                    adds=[bak1],
                    baks=[bak2, bak3])
    assert serder.raw == (b'{"v":"KERI10JSON0000d8_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
                          b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"4","t":"vrt","bt":"3","br":[],'
                          b'"ba":["EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc"]}')

    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    sn=4,
                    toad=2,
                    adds=[bak1, bak2, bak3],
                    baks=[])
    assert serder.raw == (b'{"v":"KERI10JSON000136_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
                          b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"4","t":"vrt","bt":"2","br":[],'
                          b'"ba":["EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc",'
                          b'"DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU",'
                          b'"Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"]}')

    serder = rotate(dig=dig,
                    regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
                    sn=4,
                    toad=3,
                    adds=[bak2, bak3],
                    baks=[bak1])
    assert serder.raw == (
        b'{"v":"KERI10JSON000107_","i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",'
        b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg","s":"4","t":"vrt","bt":"3","br":[],'
        b'"ba":["DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU","Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"]}')

    # invalid dupe add
    with pytest.raises(ValueError):
        rotate(dig=dig,
               regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
               sn=4,
               baks=[bak2, bak3],
               adds=[bak2])

    # invalid dupe add
    with pytest.raises(ValueError):
        rotate(dig=dig,
               regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
               sn=4,
               baks=[bak3],
               cuts=[bak2, bak3])

    # invalid toad
    with pytest.raises(ValueError):
        rotate(dig=dig,
               regk="EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw",
               sn=5,
               toad=3,
               adds=[bak2, bak3],
               baks=[])

    """ End Test """


def test_simple_issue_revoke():
    vcdig = "DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM"
    regk = "EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw"
    dig = "EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg"

    serder = issue(vcdig=vcdig, regk=regk)
    assert serder.raw == (b'{"v":"KERI10JSON000092_","i":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"0",'
                          b'"t":"iss","ri":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw"}')

    serder = revoke(vcdig=vcdig, dig=dig)
    assert serder.raw == (
        b'{"v":"KERI10JSON000091_","i":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"1","t":"rev",'
        b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg"}')

    """ End Test """


def test_backer_issue_revoke():
    vcdig = "DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM"
    regk = "EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw"
    sn = 3
    regd = "Ezpq06UecHwzy-K9FpNoRxCJp2wIGM9u2Edk-PLMZ1H4"
    dig = "EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg"

    serder = backerIssue(vcdig=vcdig, regk=regk, regsn=sn, regd=regd)
    assert serder.raw == (
        b'{"v":"KERI10JSON000105_","i":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM",'
        b'"ii":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw","s":"0","t":"bis",'
        b'"ra":{"i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw","s":3,'
        b'"d":"Ezpq06UecHwzy-K9FpNoRxCJp2wIGM9u2Edk-PLMZ1H4"}}')

    serder = backerRevoke(vcdig=vcdig, regk=regk, regsn=sn, regd=regd, dig=dig)
    assert serder.raw == (
        b'{"v":"KERI10JSON000104_","i":"DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM","s":"1","t":"brv",'
        b'"p":"EY2L3ycqK9645aEeQKP941xojSiuiHsw4Y6yTW-PmsBg",'
        b'"ra":{"i":"EE3Xv6CWwEMpW-99rhPD9IHFCR2LN5ienLVI8yG5faBw","s":3,'
        b'"d":"Ezpq06UecHwzy-K9FpNoRxCJp2wIGM9u2Edk-PLMZ1H4"}}')

    """ End Test """


def test_prefixer():
    pre = "DntNTPnDFBnmlO6J44LXCrzZTAmpe-82b7BmQGtL4QhM"
    vs = Versify(version=Version, kind=Serials.json, size=0)

    with pytest.raises(EmptyMaterialError):
        prefixer = Prefixer()

    # vcp, backers allowed no backers
    ked = dict(v=vs,
               i="",
               ii=pre,
               s="{:x}".format(0),
               t=Ilks.vcp,
               c=[],
               b=[]
               )
    prefixer = Prefixer(ked=ked, code=MtrDex.Blake3_256)
    assert prefixer.qb64 == "E_TB9WKVB4Zx-Wu3-u1_RQWy2ZrDccaOj2xUpHQcg0MA"
    assert prefixer.verify(ked=ked) is True
    assert prefixer.verify(ked=ked, prefixed=True) is False

    # Invalid event type
    ked = dict(v=vs,
               i="",
               ii=pre,
               s="{:x}".format(0),
               t=Ilks.iss,
               c=[],
               b=[]
               )
    with pytest.raises(DerivationError):
        prefixer = Prefixer(ked=ked, code=MtrDex.Blake3_256)

    # vcp, no backers allowed
    ked = dict(v=vs,
               i="",
               ii=pre,
               s="{:x}".format(0),
               t=Ilks.vcp,
               c=[TraitDex.NoBackers],
               b=[]
               )
    prefixer = Prefixer(ked=ked, code=MtrDex.Blake3_256)
    assert prefixer.qb64 == "EEDVlhKzGXA6C7n1igQF8m4WfTAEuwuvitgoM4DI3iCs"
    assert prefixer.verify(ked=ked) is True
    assert prefixer.verify(ked=ked, prefixed=True) is False

    bak1 = "EXvR3p8V95W8J7Ui4-mEzZ79S-A1esAnJo1Kmzq80Jkc"
    bak2 = "DSEpNJeSJjxo6oAxkNE8eCOJg2HRPstqkeHWBAvN9XNU"
    bak3 = "Dvxo-P4W_Z0xXTfoA3_4DMPn7oi0mLCElOWJDpC0nQXw"

    # vcp, one backer
    ked = dict(v=vs,
               i="",
               ii=pre,
               s="{:x}".format(0),
               t=Ilks.vcp,
               c=[],
               b=[bak1]
               )
    prefixer = Prefixer(ked=ked, code=MtrDex.Blake3_256)
    assert prefixer.qb64 == "E_e9zbZI8WCMNoaY1b-3aEVB59M6dc2Br8EDJ1_ozK-8"
    assert prefixer.verify(ked=ked) is True
    assert prefixer.verify(ked=ked, prefixed=True) is False

    # vcp, many backers
    ked = dict(v=vs,
               i="",
               ii=pre,
               s="{:x}".format(0),
               t=Ilks.vcp,
               c=[],
               b=[bak1, bak2, bak3]
               )
    prefixer = Prefixer(ked=ked, code=MtrDex.Blake3_256)
    assert prefixer.qb64 == "EEuFeIT3_0_IAaNg8D-5AxO6UtQCmD17n77iksL048Go"
    assert prefixer.verify(ked=ked) is True
    assert prefixer.verify(ked=ked, prefixed=True) is False

    """ End Test """


def test_tever():
    with pytest.raises(TypeError):
        Tever()

    # registry with no backers, invalid anchor
    with dbing.openDB() as db, keeping.openKS() as kpr, viring.openDB() as reg:
        hab = buildHab(db, kpr)
        vcp = eventing.incept(hab.pre,
                              baks=[],
                              toad=0,
                              cnfg=[],
                              code=MtrDex.Blake3_256)
        regk = vcp.pre
        assert regk == "EQm5xam50g9di3k-qpqq8DkxD--Eapo-1JwCbauzF99k"
        assert vcp.dig == "E8ZAv8TRo12im4Ve8BbMEDc6TSgdA5Bk-UE6bjn-B_4U"
        assert vcp.ked["ii"] == hab.pre

        # anchor to nothing, exception expected
        anc = SealEvent(i=regk, s="0", d="")

        # invalid seal sn
        with pytest.raises(ValidationError):
            Tever(serder=vcp, anchor=anc, db=db, reger=reg)
        dgkey = dgKey(pre=regk, dig=vcp.dig)

        assert reg.getTvt(dgkey) is None
        assert reg.getTae(snKey(pre=regk, sn=0)) is None
        assert reg.getTel(snKey(pre=regk, sn=0)) is None
        assert (reg.getAnc(dgkey)) is None

    # registry with no backers
    with dbing.openDB() as db, keeping.openKS() as kpr, viring.openDB() as reg:
        hab = buildHab(db, kpr)
        vcp = eventing.incept(hab.pre,
                              baks=[],
                              toad=0,
                              cnfg=[],
                              code=MtrDex.Blake3_256)
        regk = vcp.pre

        # anchoring event not in db, exception and escrow
        anc = SealEvent(i=regk, s="1", d="")
        with pytest.raises(MissingAnchorError):
            Tever(serder=vcp, anchor=anc, db=db, reger=reg)
        dgkey = dgKey(pre=regk, dig=vcp.dig)
        assert reg.getTvt(dgkey) == (b'{"v":"KERI10JSON0000a9_",'
                                     b'"i":"EQm5xam50g9di3k-qpqq8DkxD--Eapo-1JwCbauzF99k",'
                                     b'"ii":"EIGo5cJoRC7xHsvuNUcd6T5zMSmte11-oNiu7KGbdD7g",'
                                     b'"s":"0","t":"vcp","c":[],"bt":"0","b":[]}')
        assert reg.getTae(snKey(pre=regk, sn=0)) == b'E8ZAv8TRo12im4Ve8BbMEDc6TSgdA5Bk-UE6bjn-B_4U'


    # registry with no backers
    with dbing.openDB() as db, keeping.openKS() as kpr, viring.openDB() as reg:
        hab = buildHab(db, kpr)
        vcp = eventing.incept(hab.pre,
                              baks=[],
                              toad=0,
                              cnfg=[],
                              code=MtrDex.Blake3_256)
        regk = vcp.pre

        # successfully anchor to a rotation event
        rseal = SealEvent(regk, vcp.ked["s"], vcp.diger.qb64)

        rot = hab.rotate(data=[rseal._asdict()])
        rotser = Serder(raw=rot)

        anc = SealEvent(i=rotser.pre, s=rotser.ked["s"], d=rotser.dig)

        tev = Tever(serder=vcp, anchor=anc, db=db, reger=reg)
        assert tev.prefixer.qb64 == regk

        dgkey = dgKey(pre=regk, dig=vcp.dig)
        assert reg.getTvt(dgkey) == (b'{"v":"KERI10JSON0000a9_",'
                                     b'"i":"EQm5xam50g9di3k-qpqq8DkxD--Eapo-1JwCbauzF99k",'
                                     b'"ii":"EIGo5cJoRC7xHsvuNUcd6T5zMSmte11-oNiu7KGbdD7g",'
                                     b'"s":"0","t":"vcp","c":[],"bt":"0","b":[]}')
        assert reg.getTel(snKey(pre=regk, sn=0)) == b'E8ZAv8TRo12im4Ve8BbMEDc6TSgdA5Bk-UE6bjn-B_4U'
        assert (reg.getAnc(dgkey)) == (b'EIGo5cJoRC7xHsvuNUcd6T5zMSmte11-oNiu7KGbdD7g0AAAAAAAAAAAAAAAAAAAAAAQEY7OvsD6'
                                       b'-caefWMpJL3tArnwlW2N58II4Zl6AGaVollY')


    # registry with backers, no signatures.  should escrow
    with dbing.openDB() as db, keeping.openKS() as kpr, viring.openDB() as reg:
        hab = buildHab(db, kpr)
        vcp = eventing.incept(hab.pre,
                              baks=["BoOcciw30IVQsaenKXpiyMVrjtPDW3KeD_6KFnSfoaqI"],
                              toad=1,
                              cnfg=[],
                              code=MtrDex.Blake3_256)
        regk = vcp.pre

        # successfully anchor to a rotation event
        rseal = SealEvent(regk, vcp.ked["s"], vcp.diger.qb64)

        rot = hab.rotate(data=[rseal._asdict()])
        rotser = Serder(raw=rot)

        anc = SealEvent(i=rotser.pre, s=rotser.ked["s"], d=rotser.dig)

        with pytest.raises(MissingWitnessSignatureError):
            Tever(serder=vcp, anchor=anc, db=db, reger=reg)

        dgkey = dgKey(pre=regk, dig=vcp.dig)
        assert reg.getTvt(dgkey) == (b'{"v":"KERI10JSON0000d7_","i":"EuwWX3zt0VKsISdcFLyOxRG-NyajF9O4J7ssrTm7Ognk",'
                                     b'"ii":"EIGo5cJoRC7xHsvuNUcd6T5zMSmte11-oNiu7KGbdD7g","s":"0","t":"vcp","c":[],'
                                     b'"bt":"1","b":["BoOcciw30IVQsaenKXpiyMVrjtPDW3KeD_6KFnSfoaqI"]}')

        assert reg.getAnc(dgkey) == (b'EIGo5cJoRC7xHsvuNUcd6T5zMSmte11-oNiu7KGbdD7g0AAAAAAAAAAAAAAAAAAAAAAQElmla15z'
                                     b'NbkRSA_8ocZjt8j8QOx-ajK4Dda3flL6LKPk')
        assert reg.getTel(snKey(pre=regk, sn=0)) is None
        assert reg.getTwe(snKey(pre=regk, sn=0)) == b'EMqlVrnhiNUE1zUgk3DBYHGseIA96AYY-NB9cuZcOzOw'

    # registry with backer and receipt
    with dbing.openDB() as db, keeping.openKS() as kpr, viring.openDB() as reg:
        valSecret = 'AgjD4nRlycmM5cPcAkfOATAp8wVldRsnc9f1tiwctXlw'

        # create receipt signer prefixer default code is non-transferable
        valSigner = Signer(qb64=valSecret, transferable=False)
        valPrefixer = Prefixer(qb64=valSigner.verfer.qb64)
        valpre = valPrefixer.qb64
        assert valpre == 'B8KY1sKmgyjAiUDdUBPNPyrSz_ad_Qf9yzhDNZlEKiMc'

        hab = buildHab(db, kpr)

        vcp = eventing.incept(hab.pre,
                              baks=[valpre],
                              toad=1,
                              cnfg=[],
                              code=MtrDex.Blake3_256)
        regk = vcp.pre
        valCigar = valSigner.sign(ser=vcp.raw, index=0)

        # successfully anchor to a rotation event
        rseal = SealEvent(regk, vcp.ked["s"], vcp.diger.qb64)

        rot = hab.rotate(data=[rseal._asdict()])
        rotser = Serder(raw=rot)

        anc = SealEvent(i=rotser.pre, s=rotser.ked["s"], d=rotser.dig)

        Tever(serder=vcp, anchor=anc, bigers=[valCigar], db=db, reger=reg)

        dgkey = dgKey(pre=regk, dig=vcp.dig)
        assert reg.getTvt(
            dgkey) == b'{"v":"KERI10JSON0000d7_","i":"ENsCdwGnrbAK_hWtKWOsnMvhsmVnFU-8OcXPmXnlDehU",' \
                      b'"ii":"EIGo5cJoRC7xHsvuNUcd6T5zMSmte11-oNiu7KGbdD7g","s":"0","t":"vcp","c":[],"bt":"1",' \
                      b'"b":["B8KY1sKmgyjAiUDdUBPNPyrSz_ad_Qf9yzhDNZlEKiMc"]}'
        assert reg.getAnc(
            dgkey) == b'EIGo5cJoRC7xHsvuNUcd6T5zMSmte11' \
                      b'-oNiu7KGbdD7g0AAAAAAAAAAAAAAAAAAAAAAQEFicLeW_bL4CPwmcDb80d9GHsUb8r7x-egZMpb-umxys'
        assert reg.getTel(snKey(pre=regk, sn=0)) == b'EgTBFJOxsKIGCYovzcRXQD6T54ouqpvcOicDERs0SVGE'
        assert reg.getTibs(dgkey) == [
            b'AAofYsyRdZK6ijXdjZ_kITyH1zEwyKibjLu-0I5vNoaOZbbc52PWP3qI7TOZ84FfKsnro1IryTKxfXYvu8e4PPDQ']
        assert reg.getTwe(snKey(pre=regk, sn=0)) is None


def buildHab(db, kpr):
    kevers = dict()
    secrets = [
        'A1-QxDkso9-MR1A8rZz_Naw6fgaAtayda8hrbkRVVu1E',
        'Alntkt3u6dDgiQxTATr01dy8M72uuaZEf9eTdM-70Gk8',
        'ArwXoACJgOleVZ2PY7kXn7rA0II0mHYDhc6WrBH8fDAc',
        'A6zz7M08-HQSFq92sJ8KJOT2cZ47x7pXFQLPB0pckB3Q',
        'AcwFTk-wgk3ZT2buPRIbK-zxgPx-TKbaegQvPEivN90Y',
        'AKuYMe09COczwf2nIoD5AE119n7GLFOVFlNLxZcKuswc',
        'AxFfJTcSuEE11FINfXMqWttkZGnUZ8KaREhrnyAXTsjw',
        'ALq-w1UKkdrppwZzGTtz4PWYEeWm0-sDHzOv5sq96xJY'
    ]
    secrecies = []
    for secret in secrets:  # convert secrets to secrecies
        secrecies.append([secret])
    # setup hab
    hab = directing.Habitat(ks=kpr, db=db, kevers=kevers, secrecies=secrecies, temp=True)
    return hab

if __name__ == "__main__":
    test_incept()
    test_rotate()
    test_simple_issue_revoke()
    test_backer_issue_revoke()
    test_prefixer()
    test_tever()
