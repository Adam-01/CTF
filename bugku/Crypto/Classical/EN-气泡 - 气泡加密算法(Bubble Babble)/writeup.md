# EN-气泡 - 气泡加密算法(Bubble Babble)

Exp:  
```python
import bubblepy

Bubble = bubblepy.BubbleBabble()

str = 'xivak-notuk-cupad-tarek-zesuk-zupid-taryk-zesak-cined-tetuk-nasuk-zoryd-tirak-zysek-zaryd-tyrik-nisyk-nenad-tituk-nysil-hepyd-tovak-zutik-cepyd-toral-husol-henud-titak-hesak-nyrud-tarik-netak-zapad-tupek-hysek-zuned-tytyk-zisuk-hyped-tymik-hysel-hepad-tomak-zysil-nunad-tytak-nirik-copud-tevok-zasyk-nypud-tyruk-niryk-henyd-tityk-zyral-nyred-taryk-zesek-corid-tipek-zysek-nunad-tytal-hitul-hepod-tovik-zurek-hupyd-tavil-hesuk-zined-tetuk-zatel-hopod-tevul-haruk-cupod-tavuk-zesol-ninid-tetok-nasyl-hopid-teryl-nusol-heped-tovuk-hasil-nenod-titek-zyryl-hiped-tivyk-cosok-zorud-tirel-hyrel-hinid-tetok-hirek-zyped-tyrel-hitul-nyrad-tarak-hotok-cuvux'

str2 = Bubble.decode(str).decode()     # str2: xivak-norok-norad-tipol-norol-nipid-tisuk-zotak-nurud-tesil-nitok-hepod-torek-cesuk-coryd-tinak-zorik-nined-tomyl-nosal-hopid-tuvuk-zomek-zupod-tovuk-zumak-zoryd-tipuk-nyruk-zepyd-tonuk-zasol-nunud-tenok-nuvyl-nevax

str3 = Bubble.decode(str2).decode()    # str3: ximil-hynyk-rotil-rytek-masal-folif-cysuh-zoboh-zobol-himok-dosyf-fizyx

str4 = Bubble.decode(str3).decode()    # str4: bugku{th1s_1s_A_Bubb13}

print(str4)
```