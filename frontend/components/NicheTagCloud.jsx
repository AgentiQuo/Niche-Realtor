export default function NicheTagCloud({ tags }) {
  return (
    <div className="flex flex-wrap gap-2 p-4">
      {tags?.map(tag => (
        <span 
          key={tag.tag_id} 
          className={`px-3 py-1 rounded-full text-sm ${tag.polarity === 'positive' ? 'bg-green-100 text-green-800' : tag.polarity === 'negative' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'}`}
        >
          {tag.name}
        </span>
      ))}
    </div>
  );
}
