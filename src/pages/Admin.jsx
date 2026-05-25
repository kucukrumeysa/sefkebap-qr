import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabaseClient'
import { useNavigate } from 'react-router-dom'

export default function Admin() {
  const [kategoriler, setKategoriler] = useState([])
  const [urunler, setUrunler] = useState([])
  const [seciliKategori, setSeciliKategori] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      if (!data.session) navigate('/login')
    })
    verileriYukle()
  }, [])

  async function verileriYukle() {
    const { data: kat } = await supabase.from('kategoriler').select('*').order('sira')
    const { data: ur } = await supabase.from('urunler').select('*').order('sira')
    setKategoriler(kat || [])
    setUrunler(ur || [])
    setSeciliKategori(kat?.[0]?.id)
    setYukleniyor(false)
  }

  async function fiyatGuncelle(id, yeniFiyat) {
    await supabase.from('urunler').update({ fiyat: yeniFiyat }).eq('id', id)
    setUrunler(prev => prev.map(u => u.id === id ? { ...u, fiyat: yeniFiyat } : u))
  }

  async function aktiflikDegistir(id, durum) {
    await supabase.from('urunler').update({ aktif: durum }).eq('id', id)
    setUrunler(prev => prev.map(u => u.id === id ? { ...u, aktif: durum } : u))
  }

  async function fotografYukle(id, dosya) {
    const uzanti = dosya.name.split('.').pop()
    const yol = `${id}.${uzanti}`
    await supabase.storage.from('urun-fotograflari').upload(yol, dosya, { upsert: true })
    const { data } = supabase.storage.from('urun-fotograflari').getPublicUrl(yol)
    await supabase.from('urunler').update({ fotograf_url: data.publicUrl }).eq('id', id)
    setUrunler(prev => prev.map(u => u.id === id ? { ...u, fotograf_url: data.publicUrl } : u))
  }

  async function cikisYap() {
    await supabase.auth.signOut()
    navigate('/login')
  }

  if (yukleniyor) return <div style={{ padding:'2rem' }}>Yükleniyor...</div>

  const gosterilecekUrunler = urunler.filter(u => u.kategori_id === seciliKategori)

  return (
    <div style={{ minHeight:'100vh', background:'#FAF7F2', padding:'2rem' }}>
      <div style={{ maxWidth:'800px', margin:'0 auto' }}>
        <div style={{ display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:'2rem' }}>
          <h1 style={{ fontFamily:'Cormorant Garamond', fontSize:'2rem', color:'#2C2C2C', margin:0 }}>
            Şef Kebap — Yönetim
          </h1>
          <button onClick={cikisYap} style={{ background:'none', border:'1px solid #ccc',
            padding:'8px 16px', borderRadius:'8px', cursor:'pointer' }}>
            Çıkış
          </button>
        </div>

        {/* Kategori sekmeleri */}
        <div style={{ display:'flex', gap:'8px', marginBottom:'1.5rem' }}>
          {kategoriler.map(k => (
            <button key={k.id} onClick={() => setSeciliKategori(k.id)}
              style={{ padding:'8px 18px', borderRadius:'20px', cursor:'pointer',
                background: seciliKategori === k.id ? '#D4AF37' : 'white',
                color: seciliKategori === k.id ? 'white' : '#2C2C2C',
                border: seciliKategori === k.id ? 'none' : '1px solid #ddd',
                fontWeight: seciliKategori === k.id ? '600' : '400' }}>
              {k.ad}
            </button>
          ))}
        </div>

        {/* Ürün listesi */}
        <div style={{ display:'flex', flexDirection:'column', gap:'12px' }}>
          {gosterilecekUrunler.map(urun => (
            <div key={urun.id} style={{ background:'white', borderRadius:'12px',
              padding:'1rem 1.25rem', display:'flex', alignItems:'center',
              gap:'1rem', border:'1px solid #eee',
              opacity: urun.aktif ? 1 : 0.5 }}>

              {/* Fotoğraf */}
              <div style={{ width:'60px', height:'60px', borderRadius:'8px',
                overflow:'hidden', flexShrink:0, background:'#f5f5f5',
                display:'flex', alignItems:'center', justifyContent:'center',
                position:'relative' }}>
                {urun.fotograf_url
                  ? <img src={urun.fotograf_url} alt={urun.ad}
                      style={{ width:'100%', height:'100%', objectFit:'cover' }} />
                  : <span style={{ fontSize:'24px' }}>🍽️</span>}
                <label style={{ position:'absolute', inset:0, cursor:'pointer',
                  display:'flex', alignItems:'flex-end', justifyContent:'center',
                  background:'rgba(0,0,0,0.3)', opacity:0, transition:'opacity 0.2s' }}
                  onMouseOver={e => e.currentTarget.style.opacity=1}
                  onMouseOut={e => e.currentTarget.style.opacity=0}>
                  <span style={{ color:'white', fontSize:'10px', paddingBottom:'4px' }}>Değiştir</span>
                  <input type="file" accept="image/*" style={{ display:'none' }}
                    onChange={e => e.target.files[0] && fotografYukle(urun.id, e.target.files[0])} />
                </label>
              </div>

              {/* İsim */}
              <div style={{ flex:1 }}>
                <p style={{ margin:0, fontWeight:'500', color:'#2C2C2C' }}>{urun.ad}</p>
              </div>

              {/* Fiyat */}
              <div style={{ display:'flex', alignItems:'center', gap:'6px' }}>
                <input
                  type="number"
                  defaultValue={urun.fiyat}
                  onBlur={e => fiyatGuncelle(urun.id, parseFloat(e.target.value))}
                  style={{ width:'80px', padding:'6px', border:'1px solid #ddd',
                    borderRadius:'6px', textAlign:'center', fontWeight:'600',
                    color:'#D4AF37', fontSize:'15px' }}
                />
                <span style={{ color:'#888', fontSize:'13px' }}>₺</span>
              </div>

              {/* Aktif toggle */}
              <button onClick={() => aktiflikDegistir(urun.id, !urun.aktif)}
                style={{ padding:'6px 12px', borderRadius:'6px', cursor:'pointer',
                  border:'none', fontSize:'12px',
                  background: urun.aktif ? '#e8f5e9' : '#ffebee',
                  color: urun.aktif ? '#2e7d32' : '#c62828' }}>
                {urun.aktif ? 'Aktif' : 'Gizli'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}