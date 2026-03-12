/** 날짜 문자열을 한국어 형식으로 포맷 */
export function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return `${d.getFullYear()}년 ${d.getMonth() + 1}월 ${d.getDate()}일`
}

/** 날짜 문자열에서 요일 포함 형식 */
export function formatDateFull(dateStr: string): string {
  const d = new Date(dateStr)
  const days = ['일', '월', '화', '수', '목', '금', '토']
  return `${d.getFullYear()}. ${d.getMonth() + 1}. ${d.getDate()}. (${days[d.getDay()]})`
}

/** 카테고리별 그라데이션 */
export const CATEGORY_GRADIENTS: Record<string, string> = {
  singer: 'from-rose-500 to-pink-700',
  dancer: 'from-violet-500 to-purple-700',
  musician: 'from-sky-500 to-blue-700',
  instrumentalist: 'from-amber-500 to-orange-700',
  orchestra: 'from-emerald-500 to-teal-700',
}

/** 카테고리별 설명 */
export const CATEGORY_DESCRIPTIONS: Record<string, string> = {
  singer: '다양한 장르의 실력파 대중가수를 만나보세요. K-POP, 발라드, R&B 등 무대를 빛낼 아티스트를 섭외해 드립니다.',
  dancer: '힙합, 현대무용, 스트릿 댄스 등 다채로운 퍼포먼스를 선보이는 댄서를 소개합니다.',
  musician: '재즈, 팝, 록 등 장르를 넘나드는 뮤지션과 함께 특별한 공연을 만들어 보세요.',
  instrumentalist: '바이올린, 피아노, 첼로 등 클래식부터 크로스오버까지, 최고의 연주자를 섭외합니다.',
  orchestra: '실내악부터 풀 오케스트라까지, 격조 높은 음악으로 행사를 완성합니다.',
}

/** 카테고리별 아이콘 SVG path */
export const CATEGORY_ICONS: Record<string, string> = {
  singer: 'M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z',
  dancer: 'M13.49 5.48c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm-3.6 13.9l1-4.4 2.1 2v6h2v-7.5l-2.1-2 .6-3A7.03 7.03 0 0017.49 13v-2c-1.9 0-3.5-.8-4.6-2l-1-1.3c-.6-.8-1.5-1.2-2.6-1.2-.6 0-1.2.2-1.7.5l-4.1 2.1v4.4h2V9.4l1.5-.8L4.49 20h2.1l1.3-5.6z',
  musician: 'M21 3v12.5a3.5 3.5 0 01-7 0 3.5 3.5 0 013.5-3.5c.54 0 1.05.12 1.5.34V6.47L9 8.6v8.9A3.5 3.5 0 012 14a3.5 3.5 0 013.5-3.5c.54 0 1.05.12 1.5.34V3l14-3z',
  instrumentalist: 'M12 3l.01 10.55c-.59-.34-1.27-.55-2-.55C7.79 13 6 14.79 6 17s1.79 4 4.01 4S14 19.21 14 17V7h4V3h-6z',
  orchestra: 'M12 3v9.28a4.39 4.39 0 00-1.5-.28C8.01 12 6 14.01 6 16.5S8.01 21 10.5 21c2.31 0 4.2-1.75 4.45-4H15V6h4V3h-7z',
}
