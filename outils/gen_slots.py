import json,re
rows=json.load(open('/tmp/sl/rows.json'))
U={'CL':'句子','VP':'动词','C':'某物','P':'某人','A':'形容词','X:langue':'语言','X:n':'名词','X:N':'名词','X:nom':'名字',
   'X:qqpart':'某处','X:âge':'数字','X:heure':'数字','X:date':'日期','X:moment':'时间','X:nationalité':'国家'}
SUBJ=r'(我|你|您|他|她|它|我们|你们|他们|她们|咱们|某人|别人|大家|自己)$'
O={}
def o(s,room=None):
    for part in s.strip().split(';'):
        part=part.strip()
        if not part: continue
        k,v=part.split('=')
        O[k.strip()]=None if v.strip()=='-' else v.split(',')
o("""verbes:41=形容词;adjectifs:28=形容词;adjectifs:70=名词;pronoms:13=句子;pronoms:34=句子;pronoms:53=句子;pronoms:80=句子;pronoms:81=句子;
pronoms:54=动词;pronoms:70=某人;pronoms:71=动词;conjonctions:3=形容词;conjonctions:4=形容词,动词;conjonctions:10=句子,动词;conjonctions:13=句子,动词;
conjonctions:23=某人;conjonctions:27=句子,动词;conjonctions:29=某人,动词;conjonctions:30=句子;conjonctions:32=动词,动词;conjonctions:34=动词,动词;
conjonctions:35=句子;conjonctions:37=句子;conjonctions:38=句子,动词;conjonctions:46=句子,动词;conjonctions:55=句子,动词;conjonctions:47=动词;
conjonctions:52=动词,动词;conjonctions:65=动词,某人,动词;conjonctions:99=动词,某人,动词;conjonctions:78=某人,动词;conjonctions:81=动词,动词;
conjonctions:84=动词,形容词;conjonctions:86=动词,动词;conjonctions:93=句子;conjonctions:98=动词,句子;prepositions:12=动词,动词;prepositions:21=某物,动词;
prepositions:24=动词,动词;prepositions:32=动词,时间;prepositions:46=时间;prepositions:83=动词,动词;adverbes:13=动词,形容词;adverbes:53=动词;adverbes:57=形容词;
courantes_1:13=句子;courantes_1:33=动词;courantes_1:36=动词;courantes_4:0=句子;courantes_4:61=动词;courantes_1:37=名词;courantes_1:58=某物,动词;courantes_1:66=动词;
courantes_2:4=句子;courantes_2:45=名词;courantes_2:60=日期;courantes_2:62=-;courantes_2:66=数字;courantes_3:3=动词,补语;courantes_3:61=形容词;courantes_3:63=日期;
courantes_4:44=-;courantes_4:45=句子,动词;courantes_4:63=动词,动词;courantes_4:66=-;courantes_4:75=句子;courantes_4:76=句子;courantes_4:85=某物;courantes_5:0=某物;
courantes_5:18=句子;courantes_5:44=动词;courantes_5:58=句子;courantes_5:61=句子;courantes_7:7=国家;courantes_7:59=某物;courantes_7:77=某物;courantes_8:4=动词;
courantes_8:20=数字;courantes_8:38=某事;courantes_8:40=某物;courantes_8:70=某处;courantes_8:81=时间;courantes_9:34=某物;courantes_9:73=某物;courantes_9:90=某物;
courantes_9:95=某物,语言;courantes_10:31=-;courantes_10:38=动词,某物;courantes_10:45=句子;courantes_10:64=某物;courantes_10:69=-;modales_1:31=某物,动词;
incises_1:26=动词,动词;incises_1:29=句子,句子;incises_1:47=某人,形容词,形容词;incises_1:72=某人,句子;incises_2:5=句子,句子;incises_2:33=句子,动词;incises_2:36=句子,动词;
incises_2:47=动词,动词;incises_2:56=句子,句子;incises_3:46=句子,句子;incises_4:33=句子,句子;
verbes_2:4=某人;verbes_2:92=某人;adverbes_2:87=某物;verbes_3:42=某人;prepositions_2:38=日期;conjonctions_2:18=动词,动词;conjonctions_2:25=动词,动词;conjonctions_2:27=动词,形容词;
verbes_4:32=某人;verbes_4:39=某人;verbes_4:97=某物;adverbes_4:17=句子;adverbes_5:32=数字;adverbes_5:53=某物;adverbes_6:27=动词,动词;verbes_10:4=某人;verbes_13:17=某人;
verbes_15:22=某物;verbes_15:97=某人;pronoms_2:21=动词;pronoms_2:24=某物;pronoms_2:25=某物;pronoms_2:30=某人;
formes_1:0=名词;formes_1:2=名词;formes_1:93=数字;formes_12:31=副词;formes_12:51=时间;formes_13:63=动词;formes_14:44=动词;formes_7:11=句子;formes_3:86=某物;formes_5:79=某物;
formes_15:35=某物;formes_6:2=某物;formes_10:40=某处;
patrons:17=句子,句子;patrons:19=句子;patrons:20=句子,句子;patrons:21=句子,句子;patrons:23=动词;patrons:25=句子,某人,动词;patrons:26=句子;patrons:27=句子;
patrons:28=形容词;patrons:30=动词,动词;patrons:32=形容词;patrons:33=动词;patrons:34=动词;patrons:35=句子;patrons:37=句子,动词;patrons:38=句子,动词;patrons:39=句子,句子;
patrons:41=句子,句子;patrons:42=句子,动词;patrons:43=句子,名词;patrons:44=句子,句子;patrons:45=动词,动词;patrons:46=动词,动词;patrons:47=句子;patrons:48=句子,句子;
patrons:49=动词,动词;patrons:50=句子,动词;patrons:52=句子,句子;patrons:53=句子,句子;patrons:36=动词;courantes_5:85=句子;courantes_1:12=动词;modales_1:78=动词;courantes_2:80=动词;modales_4:59=动词;modales_4:72=动词;modales_5:65=动词;modales_2:49=动词""")
out={};bad=[]
for room,i,w,f,u,n in rows:
    k=f"{room}:{i}"
    if k in O: lab=O[k]
    elif room.startswith('formes_'): lab=['某人']*n
    elif n==2 and f.startswith('[qn],') and u==['CL']: lab=['某人','动词']
    elif len(u)==n and all(x in U for x in u): lab=[U[x] for x in u]
    elif n==1 and u and len(set(u))==1 and u[0] in U: lab=[U[u[0]]]
    else: bad.append((k,w,f,u,n)); continue
    if lab is not None:
        if len(lab)!=n: bad.append(('LEN',k,w,lab)); continue
        # sujet déjà présent devant la case : la proposition se réduit au verbe
        parts=re.split('(…+)',w); j=0; L=[]
        for p_i,p in enumerate(parts):
            if p.startswith('…'):
                l=lab[j]; j+=1
                if l=='句子' and k not in O and re.search(SUBJ,re.sub(r'^.*?让','',parts[p_i-1]) if '让' in parts[p_i-1] else parts[p_i-1]): l='动词'
                if l=='某物' and k not in O and re.search(r'faire \[qc\]',f): l='动词'
                L.append(l)
        lab=L
    out[k]=[w,lab]
print(len(out),len(bad))
for b in bad: print(b)
json.dump(out,open('/home/claude/zh/slots_zh.json','w'),ensure_ascii=False,indent=0)
import collections
print(collections.Counter(l for w,lab in out.values() if lab for l in lab))
