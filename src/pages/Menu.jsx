import { useEffect, useState } from 'react'
import { supabase } from '../lib/supabaseClient'

const IKRAMLAR = 'Salata, Közlenmiş Mantar, Humus, Soğan Salatası, Yeşillik, Ezme ve Yoğurtlu Patlıcan'

export default function Menu() {
  const [kategoriler, setKategoriler] = useState([])
  const [urunler, setUrunler] = useState([])
  const [seciliKategori, setSeciliKategori] = useState(null)
  const [yukleniyor, setYukleniyor] = useState(true)

  useEffect(() => {
    async function yukle() {
      const { data: kat } = await supabase.from('kategoriler').select('*').order('sira')
      const { data: ur } = await supabase.from('urunler').select('*').eq('aktif', true).order('sira')
      setKategoriler(kat || [])
      setUrunler(ur || [])
      setSeciliKategori(kat?.[0]?.id)
      setYukleniyor(false)
    }
    yukle()
  }, [])

  const gosterilecek = urunler.filter(u => u.kategori_id === seciliKategori)
  const aktifKat = kategoriler.find(k => k.id === seciliKategori)

  if (yukleniyor) return (
    <div style={{
      minHeight: '100vh', background: '#FAF7F2',
      display: 'flex', alignItems: 'center', justifyContent: 'center'
    }}>
      <p style={{ fontFamily: 'Cormorant Garamond, serif', fontSize: '1.5rem', color: '#D4AF37' }}>
        Menü yükleniyor...
      </p>
    </div>
  )

  return (
    <div style={{ minHeight: '100vh', background: '#FAF7F2', fontFamily: 'Inter, sans-serif' }}>

      {/* Google Fonts */}
      <link
        href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500&family=Montserrat:wght@400;500;600&display=swap"
        rel="stylesheet"
      />

      {/* Header */}
      <div style={{
        background: '#2C2C2C',
        padding: '2rem 1rem 1.5rem',
        textAlign: 'center',
        position: 'relative'
      }}>
        {/* Logo alanı */}
        <div style={{ marginBottom: '0.75rem' }}>
          <img
            src="/logo.webp"
            alt="Şef Kebap Logo"
            style={{ height: '80px', objectFit: 'contain' }}
            onError={e => { e.target.style.display = 'none' }}
          />
        </div>
        <h1 style={{
          fontFamily: 'Cormorant Garamond, serif',
          fontSize: 'clamp(2rem, 6vw, 3rem)',
          color: '#D4AF37',
          margin: 0,
          letterSpacing: '0.05em',
          fontWeight: 600
        }}>
          ŞEF KEBAP
        </h1>
        <p style={{
          fontFamily: 'Montserrat, sans-serif',
          fontSize: '0.7rem',
          color: '#888',
          letterSpacing: '0.2em',
          margin: '0.4rem 0 0',
          textTransform: 'uppercase'
        }}>
          Lezzet & Gelenek
        </p>

        {/* Altın çizgi */}
        <div style={{
          width: '60px', height: '2px',
          background: '#D4AF37',
          margin: '1rem auto 0'
        }} />
      </div>

      {/* İkram notu */}
      <div style={{
        background: '#2C2C2C',
        borderTop: '1px solid #3a3a3a',
        padding: '0.85rem 1.5rem',
        textAlign: 'center'
      }}>
        <p style={{
          fontFamily: 'Inter, sans-serif',
          fontSize: '0.72rem',
          color: '#aaa',
          margin: 0,
          lineHeight: 1.6
        }}>
          <span style={{ color: '#D4AF37', fontWeight: 500 }}>🎁 İkramlarımız: </span>
          {IKRAMLAR} — ana yemeklerin yanında ikram olarak sunulmaktadır.
        </p>
      </div>

      {/* Kategori sekmeleri */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: '8px',
        padding: '1.5rem 1rem 0',
        flexWrap: 'wrap'
      }}>
        {kategoriler.map(k => (
          <button
            key={k.id}
            onClick={() => setSeciliKategori(k.id)}
            style={{
              padding: '10px 22px',
              borderRadius: '30px',
              cursor: 'pointer',
              fontFamily: 'Montserrat, sans-serif',
              fontSize: '0.75rem',
              fontWeight: 600,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              border: seciliKategori === k.id ? 'none' : '1px solid #D4AF37',
              background: seciliKategori === k.id ? '#D4AF37' : 'transparent',
              color: seciliKategori === k.id ? '#2C2C2C' : '#D4AF37',
              transition: 'all 0.25s ease'
            }}
          >
            {k.ad}
          </button>
        ))}
      </div>

      {/* Kategori başlığı */}
      <div style={{ textAlign: 'center', padding: '1.5rem 1rem 0.5rem' }}>
        <h2 style={{
          fontFamily: 'Cormorant Garamond, serif',
          fontSize: 'clamp(1.6rem, 5vw, 2.2rem)',
          color: '#2C2C2C',
          margin: 0,
          fontWeight: 600
        }}>
          {aktifKat?.ad}
        </h2>
        <div style={{ width: '40px', height: '1px', background: '#D4AF37', margin: '0.5rem auto 0' }} />
      </div>

      {/* Ürün listesi */}
      <div style={{
        maxWidth: '700px',
        margin: '0 auto',
        padding: '1rem 1rem 4rem'
      }}>
        {gosterilecek.map((urun, i) => (
          <div
            key={urun.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              padding: '1rem 0',
              borderBottom: '1px solid #E8E3DA',
              animation: `fadeIn 0.3s ease ${i * 0.04}s both`
            }}
          >
            {/* Fotoğraf */}
            {urun.fotograf_url && (
              <div style={{
                width: '70px', height: '70px',
                borderRadius: '10px',
                overflow: 'hidden',
                flexShrink: 0,
                border: '1px solid #E8E3DA'
              }}>
                <img
                  src={urun.fotograf_url}
                  alt={urun.ad}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </div>
            )}

            {/* İsim ve açıklama */}
            <div style={{ flex: 1 }}>
              <p style={{
                fontFamily: 'Cormorant Garamond, serif',
                fontSize: 'clamp(1rem, 3vw, 1.15rem)',
                color: '#2C2C2C',
                margin: 0,
                fontWeight: 600,
                lineHeight: 1.3
              }}>
                {urun.ad}
              </p>
              {urun.aciklama && (
                <p style={{
                  fontFamily: 'Inter, sans-serif',
                  fontSize: '0.75rem',
                  color: '#888',
                  margin: '3px 0 0',
                  lineHeight: 1.4
                }}>
                  {urun.aciklama}
                </p>
              )}
            </div>

            {/* Fiyat */}
            <div style={{ flexShrink: 0, textAlign: 'right' }}>
              <span style={{
                fontFamily: 'Montserrat, sans-serif',
                fontSize: 'clamp(1rem, 3vw, 1.15rem)',
                fontWeight: 600,
                color: '#D4AF37'
              }}>
                {urun.fiyat} ₺
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div style={{
        background: '#2C2C2C',
        textAlign: 'center',
        padding: '1.5rem',
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0
      }}>
        <p style={{
          fontFamily: 'Montserrat, sans-serif',
          fontSize: '0.65rem',
          color: '#555',
          margin: 0,
          letterSpacing: '0.1em',
          textTransform: 'uppercase'
        }}>
          Afiyet Olsun
        </p>
      </div>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  )
}