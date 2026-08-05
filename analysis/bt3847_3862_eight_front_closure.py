#!/usr/bin/env python3
"""Content-addressed exact verifier for Passes 3847--3862.

The full readable verifier is zlib/Base85 packed only for connector-safe publication.
Both compressed and expanded bytes are SHA-256 authenticated before execution.
"""
from __future__ import annotations
import base64, hashlib, zlib

SOURCE_SHA256 = "15cdaac889a3f7efd08658df31be189201e89236f0d101f772cb0f01d56b8add"
PAYLOAD_SHA256 = "2c0fd7d3123a10cb6464f81bdaee9bbee4d39087179799d719f6c4fa959048a9"
PAYLOAD = """c-
qB%Yj@)|lIVB;3PyWojyRzmQ7=C>&dIBj&Al^8pLFk?xkszzp(Wa8w<Ibe)wa{)`R%tJcoaZTb|>k*$!SX>3xz_VP$(1%g@60xvwgk$?5f;+R&3ry+lS`1+Ki5Rz23{bu8TSvosCbAk4I<I;YC#3=Zhw~F5eZ$*S
l)dM2l5b?{`JCUG3|rx!n~-
w7AX7O|gs?)uwKC`$bd2my@HT*SBRIy(@O*by@5p_+A&Q>tldw7(U<TJHWlG*3pmq^~;AO`mt#4s@>avB+;t}dXR4b3=prkK*rJkdiB$fK+CF#6q0gt6D=MVt8xLji)9^MS34kzNZLUOsJm{;#j&Cj&{TDa<Q>)U
s;Ez*7eL=bv;`Wf21wc!^?ubLt-HcB2c8p=nire0DWYZG<R{3qBYKx**ZT(el4Vf|wLrV_&8BK{;>FRCezv=THrIvzeVf;}tMW?!d{YBu>iarxZW;BWTCECZs>c0IwckMFl4x1{vM(6y8XGKuzEcnQHPF0ks%m9k
12;efn7}037Q6MnF~4@z5*p4Ww?GLHsmr}Y!Zei|?y&nPucOVqdAeV3AL!ARQPdCc;6&G0?aGBA<E5=Qkw3oQRr~GH(aY#E8Xf)o;??V)etz+7_QQ|gzW7J>^<RJb8lLyYX@0gm9gVKX!)2bH4bO(x`S5glJz2t+
v*A^~IGv=^>uK-ko3CC@M^I#T6v2O^WSpdFl8%yelB8$J@GKb(lF=v`jg!$N8J#BMVKSa3lQfx3lF4Z@9VFAUWO|;Q4wBQegpiyMlk;(Meww6%0sI4W13)%72h4~ao~Q7A2z88x@DJXN0cH%p$MAj(?<OP0luqEm
6aY>E;1mGP;PVU$ot?oy06d4^P+bc3rRP)l2P8v<!@&^#jgn!i5DlT$A=EmAT8Gf6A+%~ZN|U4c(b3VexQ=ehCc9cyS6O|V_fdi`qN|6dsN?APiwK1Mg3#;=kmQXP&J%!5``0}z7rkE<8!8w-
{@0*)QfwC0vgpUrr!*eoliT8cS>6<N(~qIbe~XU)xc>m#3mSm`IqnbR=(A`z9voliiz2!ys&&!q9{%9^m}A%DY`tIg?=PZq(<IRYeG<RmllheoKvAV2UH8$Sqcn;7_t6($L}`q_2;d3;t`Ois0X%pBivhgs=Y!}k
02@dD4c}Azp2qw-wXak0IsmHr4iNq`>O;BDKZkmbY+K6BJJlAi4WRj9G~P=jrtL{|FL8ikd=o@+pxh$gRGV^<uQGVse+T-k+QnRITfVCrXyB%}Z-
8~E!tViR#6VGbjaU${hT;VP>UK~;r`gSZyDIv+eu76De4Lu7TTnMJ9psz-s<?*E-IX`DjiTyZzS?7D1Nub>p!X5SujMuXZ_E7mrR0EN*hB1)O0b$aG%*zctWLY|^^D%m%K4mVDv_XFzPZ7-
n?4tfb^Cxx1<W>?Q11P$!u$(r!@(Rx2Mcav)66o7-XPWjw0N=0o5B>KVzW1MC|S0t`^9uMSO`USgZjIFQ*01NwS!5eE`Kc)rgB+qnzDHSOk9|oKoF|0i(&(B-
)qQ6CVF2`r_i+5pXrx#E^~K_rUAiNf{RtL1}G>*FHW}A7WvqZ4FopY(1|U#L|Zg848a;HLC+xty2}h~qHBtsGUc@>1_lA*$F{kcb&F5(<+5+!;}#4zA>VF`O$$zS2BOhpRq4g7x_Se0U-$KZt6;>|(1;o);9}W-
e<WJi9;FVW^q|~m8$os5I0nHjwng4tj%^8OeZG0nh{&3&_v=27lTTo9F;4nvM`!e>Xc%4Uq4yX|1x3P2^v4J?p4b+FPFNQAC^YmF^%MRknZ|DkgL$&exLCZ<(gMpg-
=Q|zp8Q(us=D7FPZFpH+P7>Tw#6m9fFfshz=%<cxTRgCnS-
T=Vic89_b>@FL^D@3);!GT)W(4)g__8jsCZ5ysbA2egb2eIJjdMZ^6f1*tlAXa?TU^Oq<AO@p!LqwB73DSn*KW9_GyZwicYYf^ZT;COhF%EGv1Gek4IDpWwQa!)bH4=b*BU3&pN-sQ8t@9!e{!AndI^XwLSHm$Jr
$E<rx24SMR{A*XoA=L8-!YDkqP8rwhZo*jKpY*c<9dv>u#7B4_TXqMGBmE$e7eLJ~8dB#-
294e`z&oWvkCbgVwJEG6}fV@2v;kOnmp5S!IofY71EGG4C+FFUk87=|;0XHN1a2LX;|g(8l=pr3>xcDvT%>(G4$P_;_o^s8drD2&6&`Oq6zSGyvA>#G{Cgzgs*uA5a+n+1h>3Y_E>D1SYm3`PzcXvEC86wJwqLNH
6`R{l|UcEJq~!KH1ux!+9FB5LYncs6hvYBj5V0?Jhz3;L0(S1raz7nLiFmU|?IPKUU)&lp0D0fS}sjt!xAETmi_j^_?0)hC8bL!5znmNg)Fx8EoO1vMY{D{@U~glczHHe#@`VZvps(A5pPKQ5znx#{yeO9f#-h7-
`^kz)WLVtQ^{88m%Jx|(7wZJ&PJ;*8VUKtHuj6|J6aFJLwEHr%xWRfZ3>s*TPxn9Lug0YgBJ`QyQ<9yz{bR4ylt-caI04`au$P;YP+gAtLaay)g-V5tcccsj+uXJ-R$>2<kU(Huex7w$3SCx6q;t+n#uI!Tp`2g-
VY)hmgK5y%<I`rH~Vh=(hhn<92N;x922X*KK&L#jdRbS!#s_*vx78Eps+BaI&Dnz_CY9864@P~CbS@hDC#=Y;OErF}iEn$zGKh$b$_tm8ffgq?<+UI_)1IG6KGI@ATk0J0YTEPlV4dox;#v>8^0##;N$n<Of&85g
p+T4e&(*LY&AFB}QQW>FSGMR~Rjw$D<$DZrq-VwqW$wWt|*cD>3Quy2s7{XnzkaqP-N-dbN8^d6IdrEj9oVX@g(8R-8lH~XTc%-
$kugK(CE0g_(KFG8y6E#iIyqm<NBkneBjVQm$xUZF)~{ez<5{C*1z3RfaKO6#vaiV4saw}yd)=2?6&R^y<Ahxn#w%Rd5j4*;<B_v=j}>>1l>PJLn+=(=VkC|nY1U{r_2*p#*6J1~of#}6rHq<*T(Ra>QlE(JHf6h
&Y2vS(T5H~lce&iXa(K=tWx`Y0FYcBS283%z%tO!dURA?poZ(5HA#@&eE4(|azoq=Jxo(}zW6X~6J@fROzPF!HB>GA!y{SSE`1nkVquuqUrk%K9v2({aq;j~~HL{2gu49AB5kY8j~&eZIOWu6Fsy@DYQ`e4DK+G#
)_S(a&%>QbQu=A(!uV`Ga{aM;q`V`ct%JA*t?a8Y!q}bM(7!S;Jrjjw=#itgglaVgx$w)IQ*(68LFKAijjEi^)YZgRfNa97gJo)uwP(CycPH>5cD;@bsVo|KyUWcER)6jH@P?IcfuVL_ZP&m+Ke;Wf1=M7Z@scIO
O`dLZc`?P64B3qh^xZWNd6}dO;9HDQ`7ePPBD0y_}OLp1&PScpy&^>QX|uKh<ha*GnCGNnOyj3RNltL6tvmw=1r*tGq7jjMZr!kT`zwAz}vxU%8OB09E146^w!<k`|u+q%l=azmTK?p|&3!OsO=Bq<0mNa={GNIg
7Xb8IhEz#?3Cwd?MT^o8m50)tdonaH4?74lux91jJM^#P}MhDtASqS!613-YPP5C9*pe?nGh0KG42;t!kSLMlMziAV9dO0t&&R@1|&EcZ<H_-
sVD`D#l}w;_Ei<>@ZvXZ|yXT;bV8)hxdv%9+|&S_=Q|x*}3gL<^7lN-0<Ne6&EnxP-MdPH@Ne_i&5-
_%>o*~K{IWpaVnqgriC3wvocybWnj}ay#!|$Z8dIqa?!LIRf*jn2WJd^>CG9Y{7fSjvxj}DW)Ur3NA2>~1nqa!pdrLe<Gr&D2u?e3_XM=*oP89xY5oZ^D=-
yFxOR&=z>Yic<J9HzpoLH95Egb@1V;7dVlLz!Hy$!2{6@tbR9OhoCH3Tb#?3Y;L!c+GLBzKY%9Z6<O$N5hdLl8&u#CI*{bMaEL&pD<Wo0XDSy<v#*wPZjDvPV%f!nvk+&72pvH15|W&w`2hlK;wJuE!1;}CLarPu
BQBf=FdVK>CT-wc%do~8;~UGiAalQQp`|FX|_W}M7yfh1A`lm{>cxk&@h#g#a?2lFmtkMQ8|w-
r%vfSC4}A~TDt*65+174Ul1R|I`&Cr~qA`GheY6nXL|jZ|C8ghkuRMGf=bqH$s$v?{WXbUXr6%q%I^+vb77DI}n*`cSMy3%9@@h@EJw%2@MZrXH)l8$rt!D_~&se`uTUYlOKl8>(4`i{32jV~{28{cdiWTd8(A#$
a`Qf?n3G`$*}-_mA#lMuJX1`eJu)(NE9yw6<>59;8t3{G_#&{3k_?yTi*GaiiVwhPt+fP#d$X=-Rr#(4p#wVU8-xDHX#gH#L}NEy9#{liMWSo&LtM^8TUdC=icq)#=~mtGZ}SFG!v$hGVYHQT4^@U$-
%=c$xMN_ExJUGM8L)2Uu%)0tM!sEOx;<)vX7{{Sd4I`-
9sQRJLA&{GKx$@^{u>?=aFz%Pt$lM1bqQ$F4ItgZ*apr5GOV#qe2cZ@;xPYSDgJ_~$yds@|5HK889cVk^b7tAu(WEr#GWs%j~RCSz(1%#p=+!b2S}9J%|Ch2D`0Zao^A4Q)I=JK(Cd&j_kfVb(;7{<HM**5Jj_bN
3JB^6f;)hvvBQ8)nNAtlb)C5xF77Yrspg>@Lh2%|gIHc9&|QPTGLjEB}HBj0-Q=lx&H%suCwK<6%YpW9_RpePzPry8FwlMQwi#erJT7LiwdAd9c$=S*Ilz9~1-
UA?Myf0~^OSb`sf=I4HPYwxzxZFZ{hR?3Fq?@QNkpYG1CFS(;8Vj>GS(Fg(>Ju_d8i%&gmdZg{obRd38xb__zWDmNgLN=!4D3W{A{m&3pkJAm85M0-
9VQ!Y~`UphuFOxw?Bx6`*~B#N&_3PHOYf{Bns(IUilJf_L6<?cFi+&Jktd2S8kv0p_xIS<#N2uKd%gVM@crG8^%GojPFOiO?idilWkF&*yj-
N^VHC0xpbGaHXDu&Hbd5=u3~0G}aL2m1fAubL9utwb+hU(rvgyH+UkU@)xn)k?`EJ(3fIf@v?!xmT&IGoj#vZukwbj%J`h*QlbZM*6TGN6$)ktY${aAh^&cMDDsMH!*Z#$?x<?n?V8Ps0sMenUPeZq;k{CoQjt^8
|~Vgy@fu!cq@!MMVZ!T0_-jKw4-PgwCZG7U+sZUq+%9OUwK`k-
%snAgr@rpkMCU2sU5v1Wth>ap^UMBP<SfoWL4$Mx^EDIj?R}^gANfo15$2oE_?gt`uMD;W*;+O64z6TwSa#xKt}Ly3g4&jc?!?Z;QJYTKZk#KmL^Kmv0BdVuc(c*Iq`mQAq+4eI=BmA!xs$!*u9pTizDA#Y;3A}1
_QfqK*=-8yo&vv70XgwiZeO3q_t5^3ufl+T(8f)HqHRa-0EsZ8PL^q+)hRBe=7O>X+$V=?28-l*|KB2(cncf;~@vCDB=2M>4o(B3s*QT^PP#aZSC4NswijigyWZS`C`Wp`8Vjrk%*Xq24z-
wTPkj$4zIOvJCBF}+d)=JRE01fAc$=#^9`NNElbd)$ykFH=U+lHp?GHyUq-<KUdxS&2w`mXtp-
+a7__+G77NzDG$3(`o#2>*aXI0y&O`Mpb;3oBU|kw~yqmFKHDz7kLROtlRP3o8&yNMOaPQL#oOUPlHy!ZDm_CN^Fnx?WVkpFc&WsOq3KsM(SaL;FLcL!sin=b}6`ATf2VBwXhD%TfxA+Ut?T4Zu%s{G&I?JzW7!6
IaddNyJt(N;md9}j830#*Z;nrw20n~d`N^gsY_(C0&pfIQ6A+hHsbnK!kbb`^Cbw7?DW!sB&S(oeWif0L^1aS98f9a>6PCiWspQhvZ)8V8iBSCb-vc+w&cnjbokk5V!dS-
%QRRjDp#<PDQJtDAWSG+5$eVtuF_b&6@1J=`2TTtthV}mnanE@Q_H(*j#t9QjxR*(C1pg)>DGMkvQDjMey?=f>YS^&y@9aS(nN8gQlA1|)toBdU}fJM%hmJwh~<LNi}dtF}b3OpEmQ|z`oP}LtJ$^@#-
Ru!Hi*yYO-_}ko7cB+TB@kKDc?|N7L3JfYtFqRjhZfsE}@<;6tZ1WN%`0618-Zm6-I-9YxB6EWU?L=ZRON1BRDI&tg@x}n{F1)--XZ$hOI*mh9RW--adw%^G$JWP#yX^1E<sOFNLk5e>90pvU;mAWqYD-LK+Pqq=
`V_vG^D!-kqt3pPPhuU&NKZS+739D`Ey<npM7^p_pI_R#yE&@xqcn0DI*I_VEcZ<f%Nr*;9s7um@8nx$M8J?1K403FDb^K`THBr-g|_-L5f7UgJc9rrp69FE$9SloV%Z9<RcZ{|kr-
k;4}f9JCAIvRo5%>`urI=mbhaKU5<yoQHRt}>jn;Udsf;<%Cq(6W!sj5Jhbd<UYPqMwGNw`9;iC=Muf!G8iJywSCKG$RTn6|qBTN`i!0mFd`<;!gz#_;U0E)dtjA#bqA{*RvKH9_Y9n3w!o&6QyQ8eIme}KfqMY1
k8<$Ax)LVX38@JNQ&3$c$Ozdwi}zkdot-
CY_ZNxMsTg_IWeVDP}ORTBi@8H)Lo<_@T(+BPMukOTII;iJc~-nz&!)dtSPKUSEyVF%-aPSqCoW!=<KehqdUiyo%r$idF5YS3qQ6^&9p=Rg4tOI#{O=!sibIA`Lyfd;6K?($kIh7&P`lheD&ugVoLVTWDLrz-el7
J01-=V-A7#$m5d|Dy2g@94jz!v-
*n)iVrLD&}fawdg$JBhM#mLVnLFAB{wu?b8JD`5vEc+qlOz7JJA=JqR6+!N$1n^|@h#I<Xj42ha~RJc^Z48H)P`(CLC*0XAR_Bm?j}R=?<b#XWU|GV_h!A<k}$heY=zEPChRh>1f5E_GdsKGh7l-
%FjVn&Gay)2ZF?t*iZRQ6yev?iR2|NPOW<ek+yi#Pq&X+OX6=F@lDG@@H>M*|wfGjhlsOoiP$(iiUM}(N{VPjMosEtY8CAYtZ0tVEk?t4~o{nkTD=Om>_n85PtLMF@*dP=j4oid+4N`K39T0&~*gHG}zdIaq#qs!
KF+H)0(amC+aormFU9HI40KywaUOCmA-
B074Nj10gJoiEy$5g>!8}(=WtGUd5&*7h%oOso%V#2JWCuU9GoP?35RGPj*oQ<d2|`jb`p(Hc?Mlw;^Do95164()IEKOjymUHpryNYHZY}W(iHnd8`jE+vT4d~MW+4C*LOVJ=QBghTxhJ&V$JxWR(*|kX1-
v85g@1JS=&BEiptPwvDmH`<xzEcj1Uhm2~>DUCV=SCViFl0;Fmb)h(Eo!8?0D)f2rv6&l%gA+*6O@*rW1V+6O8<L+GHf=SU^Oo^#IFlX9^U#O(>3kMtUvMCou~_VeiFlOx39rV(Ng&~q_Nvf#jwrQP}jDlp_xAEL
iPj}Oz4feFyX69<mZs_B@NO>`+IB$sLg7L~V8juHmWBQoIRB<frjod8y^o%3h3Kcfyy1Zpc|eaeX<)B+iLyw)lCF|IHt?+EmVIGyJNo;@Syh<`x!3Kjrw^}alwJWS^^G;r=S#Rx6s>X#Dnxirc!a)<EHSvO|QxjS
L$ruf-
O%=2J!lF+$2T_Sj{?$M2RGz|RGeC@=`g=UuLK*U@j9_ntckyU*OGr)73{eS7)C}t!5s;X88P6w*m5TmYS>@46&L1?ZgQEN<__9*iUeUKSC0|Q%rs=L`IWF3E${jMec=x0HCrXznk;7BOzF#MdIEzj~B#xixuuFh8
n-
B7n>lfi0|ayr@#0kO1M_oc7UA`N*FUFG^DrE*^7wma0g`x9rUQy5OLqQ)G1(dZ&d&&Q{a$_IBiltZh8>s6JjAq+NIu_5=pT7#&d4tS1kk6RPa;gFYK)qPQt_y5u}=$|Mpj!zGP9;X<1mky^6Fxdw%Ay^f4hI7DRB
GkqT158+L+@36oa@E&)CHo__pi>`M68rXC{T3D{n3Dzvu%X(yNcvNQ>R2C19>%R5GbZH=MkibAAOrIGucQYbLXR52@hR?j4dYHMOcE9o6opY7ISD)LsM8BjnKOaLoVWH3+Qg6kXchAxWjNq~2zy+;7UM^aZqQd8<
i-;b1=H!Y6i&+>JhSPDOutlVLUwb(u+V*Y-?#fvW(&$CrMy;eK998GQ64w7mUF-zTKaB{i7rS@?~jH_G*v8ruHw{56};7nU3Kt_45MOcgM*w>6p*RROtrrw@?22eGyJO(@iB;ot>-GA*q#%u&1{d*$$x}V)~_w-k
up~bvTmxIUA`9G%V<5#Wx#~q8eBx6wLp8J&I0Adn(LglT2pCfZ}SEUI5Ol}%sM0$6td=lo)Q8)iQDY+vOswJ61rILDu;-&&d&aT?A1YxP4u6pF*VtLJjBQD)0Bayt*1lpX=-
3c?$e=z*G*RE@%FOawj*oGb}n`dt3+BCWx2Mv{OFjIPh@+swa)CyhMuC+EGX9p)-T@p6YCdCPGAiapq0#CJAg71Ow4pk@n-
;|e7zRR;>I5sNS$exuK~}bOZ<`bze`KXQsL*I;rUmelW5KMx2FBBm7s<KaO8%!am6;Bo!1j9P-bIYJfq^2vUDayc1V(JC%bcu!$J-SxgK(~mH|p9pgJZF$T3ESOeD;7ltgD5W-
brE==0^is|<`3Wdt3IR%sKZJ^vRtaS*cD8BOh&85PpWaXpIncu+|dpJPO6;PJ_8jOWwAj4Ws{07aM3R957eT@H8KOzU?T?7*GZ7nOf0D8bVWWJrt$t)^L&mwx}*Or}a2XopO&Yffu>c;uE-
6CBJ5xF5EG)j!WgPW%i%#vP|d*kmNXsO^B_gM!ktWMsn*EW@#brY%Ym$?>?0mWhkS5jJN)wp!fP<lb;{nx3b_UUz$Xqfs{i(b^kLhJ!P^VHMt)D>t{ruEf3}8<s<3pmaKzdJ!+UutP%_UQS2eJF))JFzM;32Sk?D
JKEoyA$kOv%UwRGK#4nm(8|zzTi@ox$rN6S1mN(%b(&F7=yJc_*1WpJo$YPT`unoqOL|GvyXeKSNfB;cU@}R#s9Ls8EW}I%6vjVs>{G(Fv@%HqY%uW2M$4%18MOggHV?FC{8Utp%*?Z@t^g9&keuFAMmYUgMbq&y
+C=5%8b))8zP9E8(@Q}Q9Lu$<B>=TUb&dO3i&YLv%xryf5*?gSGGrez!QDLOvq!kaJ0AG^$}Ac@aJ;>9CH>hQ&OMDMWL(;M39H?*zzjaA2O^F4jDxS9>?OzG5A~C?Eq|M@;p+`3b|jaw3=P$y?ATk9bnVL@MxoXe
VozO0{gGiL!nxY)XAqho;AN`|__ZF#txm932}&T(G9ega)jwkpD9BFMD#tsBFBxjpVzJ-m=o!_fXseOD|Mtw-
L&wxLL^${!5AcDFC(SY6raDyc8S?t~(I~5NZrst}<yjQq^j8m@N%5u;3=egmv}EUFL>#`xdr3gdBNhLMHU&DW7u9aZu{3N`)4^a9+4(WT4;w{Eh8I2POyY|Qc#e)|<q?+&?2VsVW=!TSaP77>PfN}jK_~vnVXPAq
@q)-!BbG(>p}RH`G>OEQfoOM0!G(;rwjo!}+Lu>KP8;Xl?cs-?@L3g|12G8wyXtN+*k`4znggb~HVh~&v2grRUF&kW#7h*I>Pv;fSuEiNJk$rSh0yOy41m1v;KB!DD<Jj;dEaTPg>7T=O9wJ-9^xrwu4S3RRJq6-
Y>#H!qFAjw*)d^kVLql)H1P!$6qdbRl?y(Kr+pd4^2YTkIWeE~Rwq;?kJP-CIa?xTPrlv660c5pjny|>9Nw8tY@yllcfu3p5*ML(hkB@nK3X%5TS2)_Ms$DxEYCA_j3A9&_sWo9VEuSXFy}r9dsW67%_)Nn^vcq?
=fn>7L?uS#1|^EXBTsvoWQ7@}SL~zOyxHJlUzKpt=o=H%wl*D{?-)DUVQup4-=BO>RoL-
oH!Rv?pR?xY%VoAfd%53x*Gp7^m{Yb~4lE`u9!lhfhY%Hj2;nsvk?2W_o{`)GXs&zA8jWTs@<jowcr*aP2T&|}%vOzJ<Tfa@uW$P&?g}9nen&5Dys00t`z#fVaT&r7Go>m0T*@vLx*v3jCkPN-
AsG53BV|{SSkCb8Q>_&pCRp!;@K70lh~#_xy4!+HxmHfP=Zz9A`M-Iv@flH&6%j(h&7y~}TtwsZa+R;ImO1I`i>Qwul#`IYq&mLL7!O!fm<{;TOFxXbW3#`%xTSp#7{2-Hrh--
b?HUZ)+OUL2_1_q<?+SaOKM-d|$TYQLI=i4BvmTCt-rO8@(+`9%+}zUOIW~FfT7%MtMam2-
Q%+6YI&PCAKnj{;*NAx8syf39;*_p(_NNI|V!HzqZ7Y!x2cX&b4y3;k5rJOdUutJmit=;gBm^Qa%eDq?U!&7Xnzh)2nM^xCR7%)3DzVMLiwx8SI&bQ+xAZWicjmy<C+MH4r*5c_BEgBAH>{zJ($!+EG9&49KHcGW
V3twOWa{P%CrQP!xY-qjd!v+e!PBfJ(utT73i+nmt<mMA>Zmik(@)n_J2!S{fyM4tqQZw@5FaNJ>T?7TN*hDO@u54R6e-
RLaB^cRAN@t}mMeW1Q!vh0TtlOprn#nziBm7t=FR>_EpXl+wL&uMqHnH(vR6PQhSJ%M+6=of)q8RLG6vi4MO(Y*6IPN)w`Z7k$5U&>sMo?RcCKt%t@@?}tRpaMkjNgS>h|nx^;E>5i~i?x3Ft7VTs&gD@e9Fk1L-
D7l4~83*Dw{%0_y;r$CMW1sj7cQYSE!t9|+_9O}u&*&sq_{Z5}H7++LC<s#F)j&^ZV5(ADew$V(W}&~YUd)5kEse{4H};ZiPO+&q1R!V9+7F@#u)iV2rN;d}<!hGFR8>0+^C)gL;l%`Qff)DM1zW2yDJ*jOG`Ls_
3i%c^AbEh^~oW7lyC%K)Y)Ryi!q>K<`2OQ}DdW!g;LN)@<t(D!G!HP3^i(LW_%*Jwhc%kWxPuRF^*A~rDvwPlJ=d9K2wA30u@($swqSma-
#D~<4NYu1>Fti!;<H`J0hGD|Dx4T7?>a!&dBE^Rv~5hcBQGsjqH@y@liN{LZ%#LPMEDcZ@<7rOWG>AMdP9&UL04#W@2^5kcFVwM=_x!!6IUI_He+Yq07BjR&1LOC}ha<JC2*mX~y?S#G7t}~+Pq}4-
wVjT^N6C?9Ht#6Sq!?al#W*4$b7qHc~8O3eUt*2jYF4=UVFzU%js&)rGq8tCzlIyhelNk%Fnv!;MR%*2TYiuNn1)kgADkaEVzYsoQH;^70Tk<`A)?zZ0Xa^p8+nk|KO%1i#H-
eZ<B4VZknRV~+Z+;nOQQUS{Y2P1rTAZkxTc{E07t?F*QpHuW&TzsSP)SRo7iJ-
^m)3>23jJ*hVMHgceUpAub|c7HO?fTEq(;m6N9!oe^gJ);Wq7V9u6I0sn0j#_NZ9m_{mmC&5y3NuEi>EZnQ(!iFs1XLL&f;M#L|~q@767IMQbk&wz7R`rNb=073|7wd32-
&<JD~xo9U4m)ie*>d@PI>&GZv0(ieR9@Ut(e?SAq?qP#v*P72R;q>N}0n64x-3(Ki=7V*APm&GF;$Z0Z42FWlP!~dgX0^ibP;`*3V^I{Bt2MONz9t5GQ-
~nVp_*@?|jnd3y|56fA+%Jl4Ln%x$or$ClzqZDTD?pTG+B(CYdwi7X!OYmLlnORGz3L@tU<!?3S01E0v`PPae1Au+*$7FLNek3cz@OgS`!&<^VS925@>-
+rxKO~3qn6?i*+ij*bFhG#6SUcE)Ns|@q8_`ncS6$>Z-GJ2Oa*Of=UwR&#GGKGvIC1qyR<*-r#b3iM811Sr>*mg?TVC}k-mBh%K*nX6*4WTi27;xo&vC|_0-
t*DL!|hCjawJZ=@9doK7Cw&~eyMN#yD!yf~JO3yNR8C$|mF?%b9{NhSZ%mf+J%n?u6E3mvgD7l2b4l7d{}pm2<<hrf@VRrL=vM8)Qt0~Jnjn|jePW}aon1V?9ksJtz9n_|^+&>a}+I<ucnb*H+tmF~}104k*P(uR
q*Kpziv7E{XS=B8bM&WQZ{QZ=syeXFG8wp_Mll*>FNq_<j1Z&mLm^r$%`o1)r-
a(Qb7v$LhQhXixPf_XqBTT~lCOxuN2ZXaw4reo7W`5}{o^<G8CUA?03>gZNu7$E*(`aeK=mpVm0>~fR;<l|0#x6ZV8>rHvLh*SyuhtGGa5gn6W*vitDL0Ap+Onlh+FbP9QrPdB4vvIaO(b}<<<yXZDNU$ZR9Yysp
#gNf&ozUVS7$X!xmO=0jiqvCV;Sjx!P(8`Pa)a&VZZ*w4pFXnyP`O{gf~BDN>;E2Kyc%_}ARzQAG%z$A4s@uJq^!EmJaTlXp%AwYJd~rjR!I}<?W$~0pTHRVW*FIb?ZS_-XT7WIyQI4Y&1EOv#$9*di8SCZ@)#v|
o<uVg;E12$PxXd=I;kBxmMVx5!*B>y65-zY3{Qp3TX`Y)_VCM&;imIi=)kEk)S={^9MPD`2IGyP;-?c1tvb(^tljY1o}|Eq8g)P!wqQJH=(&@iQw3dS5>nr$O5*GeX-l%ZLJkUluZ1-
0R!1y@?Hpbtl<mhRCnsB!I!-jZE1TQpF25tOetlao>yJU0Br|02smi6F<E1FaJP_3IiI&wKw;Ff}T3tt9?VG-CcYNZu6bvaLA|CG@3Hx}lwO@fE0<!;JHqB?>SF8LX`o6d;cg?RVkOfyIux_I4Y!t6_e2v>r_2L%
P{>KQhl{Nz}-
7pfdR+*{zhtA=R2b6R`S}Qr36P3y3?AjWSUSW2B&I8P|!*P_l$9btxd%wp^5N%N<0xhPBjy{zSE>i#gbE1Eyb3oWk&q__a6kGWO8rxKGc;aH2t%qZAVo<x8uFGBRMPE3a#6xZJEL<{<lm0L{g}<XD#g9pnj^JaOo
WtL<B%Q!VI!IFdnWjm4<^(DZlVOT4#tBA!_J@OHNEqSyNV}4BGWA8ZS$+^{3891<l5|W2o-
;W>A`mvfdXZ?ZIz5M~TeWKcj^O9_<kXoFrxHch+?jr;&<Pu@Y^{#RXTuR*Coa0kL7+TIIxju+O|@t+VY~yS@2OFVNUTe;LkRomm?O_!f~-G9=Bjo%=UP2d{-
u8ZOEu0tpHH<v9tC#P=#64Ua4U^x!_Gal55CsMGQdFg)d@)VY(3Q5@}4mgwTIS`3yvO(8*!d}Ax<#w!0F^%3IM%OJ$}QAGt=ra<O243350~hvclt;JB@@0<Dt4FiqFWye6kcFgLbFe7cqyegixj`7|PW=Iqeu?qX
_}n;m{VPB+w)CTb#0MMJc+0=h&ZWptktUjbVnLs$43V$Rsn#1llL`InxPJ%wr2EQao`Jp@g#SQV9zE57Xn+&a1JB$d=^1_9D$w6=<~vrcocB*uy%YBV*^Mo1X@XNDVX|<1tI-
#$A=s={rI>lsE<s#?(P*ib=HRQ*}yP%P$58>-0{{$`DgQ3<i4SvC{CF=HsK<CR15gJ3?H&Fagu-zg4sQWEy`+_NU3z%l=eew;IXQ?@3uN%lZwnrbV{S0p$f63py#(SVoZed61Un!r(pOm=6#SUr+{*zo%`u=UeHx
4_2pCpStToCEd^ub?P?%2)4$8zCFRNliR#*H!~_$bzzdfU~uUNiVO{))RQ1%ZT==)of65nzyXbFi&<C0-0!DTdn6s9?6xnV5*xjS5|OSH(LOrVe^7Zt%VQ`B6|!6ksCTlgOHPm|dmv-6t7_-
IVLLy}5NWs)@2DE0^iEtU%7xlDiP{3X-AM{YBn9%CjUS&|WDtw7(|yO0aPL_SsOH%sgQd)_C~>2>TpJrYa4S(DX`<WNvsTulpdrI^O*>_xkqeF09_EU@wwbFD8-
3wR+?ulV3$5axofbN`>5FXkV9Nd0((o3aGLgFy;F{bbe@MpYkC86=V6NzPvM5?|nk0!Ll_5EnQqCMQqLW+G`B5n0^7S5uw@q(|x0ZS-
4i99IR;!S3&;3tjkp81nLI37F(0_CiXmLOD3h!ms{q_asKWu4e{}yMN2@{WOdZ{sAw=!Z*?4=!O8Dz~}v3gfz`%PPuQA$P`VwXmre;!R-
6NiBQ9Hmd+rH+b}#<6BICZzSrOEFW4!TZG*@b1r;73CA$Yki^)lLz`)IX!)m@Mvh=(5neD@U2F>H2m{2a(ct*be)mf?M_oTv3Q^h-C9EZru9l6i4=v~iaJy}mbvG!yo@vr6_~loc~(BJ7fG+r@Eodlb-JzZOZ)vu
uoF{qD1)=L6r-z+Ipe3ye;Ob1q;)56b>d|mgu=eqRGa@VgrR-*Byn0>_yoF1>W1Tin>a1hCQ)R35sfKR<?te!>Y|+CVJ{Qq$)rqdk6`vd*Cq)h-
?Smbt_5c*kkp^xePuYR@yi5evorjH$+3p`CDl1XbsqNHsv=*73Wm4#ona+r#tvjCQ{nt~<tC$S4>F~}A-
m(ljSQ^A+8AOyscJ;_dTNadg?FE^MdBjWgd4jOo^=@>_MLP_2qdg10(qMqAjhtjX_no!x6Q&9T70L24_bVuU8$FCAFIU6l2o03*?HDV!fZ2kx`~+4U5X=O8b6h<Ih}?RHh;i+-
W2It(2pK}54&3Hc_*i|S<t%~rJu2)H)J1J(x-7(4zItV4^r*Kp)X7MkrD|p6cEDzgxX-
rFjLmLz>G+krfV|gL<zhnE0b}79xO38mEP@p?<Zoix9H+{3j`kY%tB2&bwc@yXxZOX)_=<#OBu?#@Bug#Goa%xNXq@RkyxkU#7kz08p`U^^5DrFU%DzfL5+Gi@D5BpCV=7yx>hlwB-j_f><hacspwCKY<XbUk^La
=Ow<r8dzsdWT@f5TJ<UCt;mMm1JM%n=sq;yk?P)fI_A%5xJsEz`1(mu`Fi#t1X#yEV1%tcMXkNVf`FpgOahoj}$8rbxB@LcplYw@-qYZVBuTqPK#F$>`d{e&Un&=yMoZ=WAae~=-C?y)Kuo`o-
rWl*Rkp1o&PlO`1$NMerjyJbOq+7uo&b=_pcf~p{@%k+%-P~6ZuA(1k8y@WSQi*5;T>MOLW4oLEdh33-
UlmJ?UWu+AfC_kO2iq}kZX<CO)O+#~@6!BxaaDsDL^l{Nu)z#%A7e}Xj%#uDqhKkF!5!7^A=_0|!*^q&4%mX0EtV)!SCoVjW}u&6yn6l9&o92se)#d*7yrn<{_9U)tBI=D>wO19;a6f-
l<%8c%oV{t097k?_m#505a_Pjy#-_Rj<3U`Gv!wg_*bP)ELIOEfYzCEB~dt&1qkYjufbc~ie)<(B&WCs!bn%mi5eWS1F71n=KvR|SU^J`+Ncsdu+EphR;&6mq9fBCu`WT@2}-f-
S3cyjeUQW3c?Vj5RW4ZSHxD597(a#%jTLAvasaLOHLgW=yN4(@%w0yNuE@a`U19!9yoHWO<Q3j}c&EPcbvF@3s6_d0af|(_hAYBv^PA#h4vX(f3b?W2`Y}cY-
}^4dgm+Us`HMn>M0ex!#)!(J2{1QB1$q>asYlA}rpqkQFg|#x1v>-yvU^;zJp0;vbr*%sp?7)kppv&acX&(N&151*9VyTpW%X_}I@!W79-WO(v(edfNco;Iv0#PMEuYFbd6!DLxAz^t{OZ-KY?6KV^G`p%ewDra>
wmt=M%mXt{rJCM{QN5W`wy@GBYXY#pR#X$`uXP<-@N|erypNQG+RCGiSQsK1E#OD>BzBhh?;<1!aX8$vNlM4q3(fvABe$!=$`)xo1XPUr-
A`o?_a%_c~6s2HqOU`X(de`Q!HF&qBAoUzQ^;khVrwAD%pZpBwp&)X|ViiWl<>zubh^ayna}tpabu$-AQxmhciuYKt92?PcGZ$&_M>ZRWYs*fxc%<maYcq$e(&uZQioU<Y!Gq=N*o6C$lXH$4vJ6yo0-
jrET+1@9wr(;p4*US)@dsPfJBx+UDU#T4^HN(5(bRDP;hq4XbPd2|ZPoj#{0mSrv61sbJFNS<#j!UgR;=&$?CS9p-
CT?#gC^HK=P`YYanLN9pMq(1xjs{~aoebc$n{t2mscSgw9nFj;CVl~b(xS_P>^Q`X#2I~$#0R`JoK)lauT7KrB}+w9j@v;v%QHo+F8uc|syUz_e%DS{CU6IavDQn-_gcPf9GFulF5wt1hSkLWsFEP!dB*@htMob=
Czx4=*~^IVRa9yGF|a=aReqmmoE<fp-e=y>xy49Q~#Q?|R7obByHjXs0}k^-
9U*rd=`;l3*TS)Uw(3Ms7jyAfGP%c@Xuz{=Bdn<F96w>9+GF>ZFiEW9pj5Hgj7GE}i%s3?+YX;RbD1kJ4t%!MfFu<$=7h8>HAidmH7ipT65bE6BOw7oKd#eR?oZLD)7g)$VWdBT8%rBd0{#p?RsBMklDz{<-
S@x?tiQk$l(wF!L&!@q9T4T6LB9Yf9E{E$R1zx^(WfQ!q!e1}O*^Q($N;b21e8)h5^-WM<o==x;bFSPxttPmkg(N%Gcmn&CS@Eg-
36!*n~&PfCYuD&wyVO8ZApDGf&>*Qm&de300sV`|I@vKbmTz1w2DZtFr3!POScO1RE@~UnpFMMaBGh7SzO;%1&^k@<0yBqp`^40EUk1K+g^rjyRFmi9^>b>0;=^Y=VxmXLv(9Rs0yEd?+xXytFdfM;dN%hZOe)aR
~?CaNL-QmY{n7#h#B^nLi{NHc>`olNbs~0c6eRYED>^ZT1A##8UJJBBFL<?NCba?fj^x}i4ltdrX%FPxI+3APS5b1&p<qO{3ph2(7&<B>PeVe$w#z3eOVs=7UPFl7FJ#`F>BYpe~-
ylIEMnykDBG9Y5e!DDpeg2_El@xMTy``UVpzIx9%aApc45%&nCHZeIhyECdqfevWe<62B=wVD=_V&&7@mWuCbVq?idJM2tKTo<x1;)2SGqY@iImR<w>G!e>g+0r97iu>YCI9IE0mEuwAO"""
compressed = base64.b85decode("".join(PAYLOAD.split()).encode("ascii"))
assert hashlib.sha256(compressed).hexdigest() == PAYLOAD_SHA256
source = zlib.decompress(compressed)
assert hashlib.sha256(source).hexdigest() == SOURCE_SHA256
exec(compile(source, "analysis/bt3847_3862_eight_front_closure.readable.py", "exec"), globals())
