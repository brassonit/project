export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 mt-auto">
      <div className="max-w-7xl mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-white font-bold text-lg mb-3">BRASS ON IT</h3>
            <p className="text-sm leading-relaxed">
              최고의 아티스트를 섭외해 드립니다.<br />
              공연 기획부터 섭외까지 원스톱 서비스.
            </p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">연락처</h4>
            <p className="text-sm">이메일: contact@brassonit.com</p>
            <p className="text-sm">전화: 02-1234-5678</p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-3">바로가기</h4>
            <ul className="text-sm space-y-1">
              <li><a href="/performances" className="hover:text-white">주요공연</a></li>
              <li><a href="/booking/singers" className="hover:text-white">섭외대행</a></li>
              <li><a href="/inquiry" className="hover:text-white">문의하기</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-sm">
          &copy; {new Date().getFullYear()} BRASS ON IT. All rights reserved.
        </div>
      </div>
    </footer>
  )
}
