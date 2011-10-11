from ROOT import gPad, TLatex

def ATLASLabel(x, y, text = None):
    
    l = TLatex(x,y,"ATLAS")
    l.SetNDC()
    l.SetTextFont(73)
    delx = 0.115*696*gPad.GetWh()/(472*gPad.GetWw())
    p = None
    if text is not None:
        p = TLatex(x+delx,y,text)
        p.SetNDC()
        p.SetTextFont(43)
    return l, p
