export default function ImageCarousel({ images }) {
  if (!images || images.length === 0) {
    return <div className="h-64 bg-gray-200 flex items-center justify-center rounded">No Images</div>;
  }
  
  return (
    <div className="carousel h-96 bg-gray-100 flex overflow-x-auto snap-x rounded">
      {images.map((img, i) => (
        <img key={i} src={img} alt={`Slide ${i}`} className="h-full object-cover snap-center flex-shrink-0 w-full" />
      ))}
    </div>
  );
}
