export default function Navbar() {
  return (
    <nav className="p-4 bg-white shadow-md flex justify-between items-center">
      <div className="font-bold text-xl">Niche Realtor</div>
      <div className="space-x-4">
        <a href="/niche" className="hover:text-blue-500">Niches</a>
        <a href="/client" className="hover:text-blue-500">Client Login</a>
      </div>
    </nav>
  );
}
