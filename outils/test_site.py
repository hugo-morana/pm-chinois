import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist"])
        pg = await b.new_page(viewport={"width":390,"height":844}, device_scale_factor=2)
        errs=[]
        pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type in ("error","warning") else None)
        pg.on("response", lambda r: errs.append("HTTP %s %s" % (r.status, r.url)) if r.status>=400 else None)
        pg.on("pageerror", lambda e: errs.append("PAGEERROR: "+str(e)))
        await pg.goto("http://localhost:8765/index.html")
        await pg.wait_for_timeout(6000)
        await pg.screenshot(path="/home/claude/zh/shot1.png")
        info = await pg.evaluate("""() => ({rooms: DATA.rooms.length, niches: DATA.rooms.reduce((a,r)=>a+r.niches.filter(Boolean).length,0), tts: 'speechSynthesis' in window, title: document.title, where: (document.querySelector('#where')||{}).textContent})""")
        print(info)
        # ouvrir une fiche
        try:
            await pg.evaluate("() => { if (typeof goTo==='function') { goTo(0,0); } if (typeof renderFiche==='function') renderFiche(); }")
            await pg.wait_for_timeout(1500)
            html = await pg.evaluate("() => (document.querySelector('.fiche')||{}).innerText || ''")
            print(html[:900])
        except Exception as e: print("fiche err", e)
        await pg.screenshot(path="/home/claude/zh/shot2.png")
        print("\n".join(errs[:20]))
        await b.close()
asyncio.run(main())
