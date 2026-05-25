import { useState } from 'react'
import { supabase } from '../lib/supabaseClient'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = useState('')
  const [sifre, setSifre] = useState('')
  const [hata, setHata] = useState('')
  const navigate = useNavigate()

  async function girisYap(e) {
    e.preventDefault()
    const { error } = await supabase.auth.signInWithPassword({ email, password: sifre })
    if (error) { setHata('Email veya şifre hatalı'); return }
    navigate('/admin')
  }

  return (
    <div style={{ minHeight:'100vh', display:'flex', alignItems:'center',
      justifyContent:'center', background:'#FAF7F2' }}>
      <form onSubmit={girisYap} style={{ background:'white', padding:'2rem',
        borderRadius:'12px', width:'320px', boxShadow:'0 2px 20px rgba(0,0,0,0.08)' }}>
        <h2 style={{ fontFamily:'Cormorant Garamond', fontSize:'1.8rem',
          color:'#2C2C2C', marginBottom:'1.5rem', textAlign:'center' }}>
          Admin Girişi
        </h2>
        {hata && <p style={{ color:'red', fontSize:'13px' }}>{hata}</p>}
        <input type="email" placeholder="Email" value={email}
          onChange={e => setEmail(e.target.value)}
          style={{ width:'100%', padding:'10px', marginBottom:'12px',
            border:'1px solid #ddd', borderRadius:'8px', boxSizing:'border-box' }} />
        <input type="password" placeholder="Şifre" value={sifre}
          onChange={e => setSifre(e.target.value)}
          style={{ width:'100%', padding:'10px', marginBottom:'16px',
            border:'1px solid #ddd', borderRadius:'8px', boxSizing:'border-box' }} />
        <button type="submit" style={{ width:'100%', padding:'12px',
          background:'#D4AF37', color:'white', border:'none',
          borderRadius:'8px', cursor:'pointer', fontWeight:'600' }}>
          Giriş Yap
        </button>
      </form>
    </div>
  )
}