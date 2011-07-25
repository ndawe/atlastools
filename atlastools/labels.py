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

"""
void myBoxText(Double_t x, Double_t y,Double_t boxsize,Int_t mcolor,char *text) 
{
  Double_t tsize=0.06;

  TLatex l; l.SetTextAlign(12); //l.SetTextSize(tsize); 
  l.SetNDC();
  l.DrawLatex(x,y,text);

  Double_t y1=y-0.25*tsize;
  Double_t y2=y+0.25*tsize;
  Double_t x2=x-0.3*tsize;
  Double_t x1=x2-boxsize;

  printf("x1= %f x2= %f y1= %f y2= %f \n",x1,x2,y1,y2);

  TPave *mbox= new TPave(x1,y1,x2,y2,0,"NDC");

  mbox->SetFillColor(mcolor);
  mbox->SetFillStyle(1001);
  mbox->Draw();

  TLine mline;
  mline.SetLineWidth(4);
  mline.SetLineColor(1);
  mline.SetLineStyle(1);
  Double_t y_new=(y1+y2)/2.;
  mline.DrawLineNDC(x1,y_new,x2,y_new);

}

void myMarkerText(Double_t x,Double_t y,Int_t color,Int_t mstyle,char *text) 
{
  //  printf("**myMarker: text= %s\ m ",text);

  Double_t tsize=0.06;
  TMarker *marker = new TMarker(x-(0.4*tsize),y,8);
  marker->SetMarkerColor(color);  marker->SetNDC();
  marker->SetMarkerStyle(mstyle);
  marker->SetMarkerSize(2.0);
  marker->Draw();

  TLatex l; l.SetTextAlign(12); //l.SetTextSize(tsize); 
  l.SetNDC();
  l.DrawLatex(x,y,text);
}
"""
